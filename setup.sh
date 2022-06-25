#!/usr/bin/env bash

ppmd=$(dirname -- $(readlink -f -- "$0"))
ln -sf ${ppmd}/ppm ~/.local/bin/ppm

mode=${1:normal}

if [ "${mode}" == "dev" ]; then
    venv="${ppmd}/.venv"

    python3 -m venv "${venv}"
    "$venv/bin/python3" -m ensurepip --upgrade
    "$venv/bin/pip3" install -r requirements_dev.txt
fi
