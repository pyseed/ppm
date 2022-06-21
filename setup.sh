#!/usr/bin/env bash

ppmd=$(dirname -- $(readlink -f -- "$0"))

ln -sf ${ppmd}/ppm ~/.local/bin/ppm
