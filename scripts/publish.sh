#!/bin/bash

python3 -m twine upload dist/*

rm -rf dist
rm -rf build
rm -rf testaton.egg-info