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

## development

```
bash ./setup.sh dev
```

when a new command is added, and in python:

- test.sh must be updated to lint the command file
  