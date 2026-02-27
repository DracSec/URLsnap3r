#!/bin/bash

python -m venv ../URLsnap3r
./bin/pip requests beautifulsoup4 playwright
./bin/playwright install
ln -s urlsnap3r.py ~/../usr/bin/urlsnap3r
