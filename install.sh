#!/bin/bash

python -m venv ../URLsnap3r
./bin/pip install requests beautifulsoup4 playwright
./bin/playwright install

echo "🌟URLsnap3r installed successfully🌟!"
echo "./bin/python https://DOMAIN"
