#!/bin/bash

python -m venv ../URLsnap3r
./bin/pip install requests beautifulsoup4 playwright
./bin/playwright install
ln -s $(pwd)/urlsnap3r.py ~/.local/bin/urlsnap3r
