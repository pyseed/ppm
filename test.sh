"./.venv/bin/python3" -m pylint ./tests

# add command scripts here
"./.venv/bin/python3" -m pylint ./bin/version
"./.venv/bin/python3" -m pylint ./bin/bootstrap

PYTHONPATH="${PYTHONPATH}:./bin" "./.venv/bin/python3" -m pytest -v -s -p no:cacheprovider
