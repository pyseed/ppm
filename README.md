# ppm

python project manager

## usage

```
bash ./setup.sh
ppm [command]
```

## commands

### bootstrap

bootstrap python project from current directory

please first prepare following actions:

- create a github project
- clone it
- cd it
- copy your template inside it

project template should have the folowing structure:

- bin/
- docs/
- src/{project_name}/ the typo should be {project_name} for bootstrap to rename with real project name
- tests/
- .gitignore
- .pylintrc
- CHANGES.txt
- LICENSE.txt
- pyproject.toml
- README.md
- requirements.dev.txt
- requirements.txt
- setup.cfg
- setup.py

following tokens will be replaced for each files:

- ${project_name}
- ${project_description}
- ${developer_fullname}
- ${developer_email}
- ${developer_login}
- ${python_requires}

for readme and license for example:

README.md:

```
(dash) ${project_name}

${project_description}
```

LICENSE.txt:

```
Copyright 2022 ${developer_fullname}

...
```

for setup.cfg/py example with a static setup.cfg and its "setup.py wrapper"

setup.cfg:

```
[metadata]
name = ${project_name}
version = 0.0.0
author = ${developer_fullname}
author_email = ${developer_email}
description = ${project_description}
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/${developer_login}/${project_name}
project_urls =
    Bug Tracker = https://github.com/${developer_login}/${project_name}/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = ${python_requires}

[options.packages.find]
where = src
```

options.python_requires will be processed by '${python_requires}' token, tokens are set with console user questions

setup.py:

```
"""
setup.py wrapper from setup.cfg
(used by pip3 install -e .)
"""
import setuptools

if __name__ == '__main__':
    setuptools.setup()
```

### setup

setup project (after bootstrap)

after this stage, you work, you ppm lint, ppm test

when you are ready for your first pre release type `ppm release minor` for 0.1.0

### lint

python linting


### test

run pytest unit tests

### release

```
release patch
```

```
release minor
```

```
release major
```

build a release: build dist + pypi upload + git tag + git push

you must be on 'master/main' branch (ppm will check this for you before)

current version is in .version.txt, semver will be incremented according to the patch/minor/major release

theres is confirmations during steps of the process

### build

build dist

this command is called by 'release' command, but you can rebuild here

### upload

upload dist

this command is called by 'release' command, but you can reupload here

## custom command

you can create a custom command in ./bin/mycommand of your current project directory

file must be executable plus bash/python adhoc shebang

you can override or replace default ppm command (if the command file has same name as the default command)

with ppmInvokeDefaultScript function, you can invoke the default command

example for setup command:

./bin/setup

```
#!/usr/bin/env bash
set -e

venv="$(pwd)/venv"

ppmInvokeDefaultScript setup
echo "example of setup override"
"$venv/bin/pip3" freeze
"$venv/bin/pip3" --version
```

## releases/upload to testpypi

to test your releases/upload to testpypi, please override default upload in your current project directory

you will upload to testpypi with `twine upload --repository testpypi dist/*`

and test your package from related https://test.pypi.org/simple/ index

./bin/upload:

```
#!/usr/bin/env bash
set -e

export $(cat .env | xargs)
cat .env | xargs

# upload to testpypi
"${VENV}/bin/python3" -m twine upload --repository testpypi dist/*

test_venv="/tmp/${PROJECT}-venv"
echo "testing latest uploaded package in temporary virtualenv ${test_venv}..."
python3 -m venv "${test_venv}"
"${test_venv}/bin/pip3" install --index-url https://test.pypi.org/simple/ --no-deps "${PROJECT}"
"${test_venv}/bin/python3" -c "import ${PROJECT}; print(${PROJECT})"
rm -r "${test_venv}"
```

## development

development setup:

```
bash ./setup.sh dev
```

linting + tests:

```
./test
```

when a new command is added as python script:

- test.sh must be updated to lint the command file
- run `./test`
