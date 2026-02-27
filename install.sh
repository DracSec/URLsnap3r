#!/bin/bash

python -m venv ../URLsnap3r
./bin/pip install requests beautifulsoup4 playwright
./bin/playwright install
echo ''
echo '🌟URLsnap3r installed successfully🌟!'
echo ''
echo '\tExecution: '
echo './bin/python urlsnap3r.py https://DOMAIN'
