<img width="975" height="178" alt="urlist3r" src="https://github.com/user-attachments/assets/4873ee0d-21d6-429f-aea5-bb32d6f6dcca" />

### URList3r.py
About
The URLsnap3r is a Python script forked from DRAGOWN/URList3r and designed for a crucial reconnaissance step of identifying hidden URLs, API endpoints, configuration paths often hardcoded within external JS files, checking the access status and taking screenshots.

#### Description

The URLsnap3r is a Python script forked from DRAGOWN/URList3r and designed for a crucial reconnaissance step of identifying hidden URLs, API endpoints, configuration paths often hardcoded within external JS files, checking the access status and taking screenshots.

By scraping a target webpage for all linked .js files and applying powerful regular expressions to their content, this tool helps uncover potential attack surfaces that might be missed by simple link scraping, providing valuable data for vulnerability analysis and screenshot each of the URLs.

#### 🛡️ Ethical Hacking & Responsible Disclosure

This tool is created for legal, authorized, and ethical security testing only.

- You must have explicit, written permission from the asset owner or be operating within the defined scope of an authorized bug bounty program before running this script against any external target.
- Do not use this tool for unauthorized, malicious, or illegal activity.
- The developer assumes no liability and encourages responsible disclosure of any vulnerabilities found.

#### Features

- Deep Link Discovery: Finds URLs and relative paths hidden deep within JavaScript code, including those defined inside variable strings.
- Automatic Resolution: Uses urllib.parse.urljoin to automatically resolve relative paths (e.g., /api/v1/user) into absolute URLs based on the source file's location.
- Robust Parsing: Leverages BeautifulSoup to reliably find all external <script src="..."> tags.
- Flexible Input: Uses argparse to accept the target URL directly as a command-line argument.
- Screenshot each of the URLs.

#### Requirements
Prerequisites

- Python 3.6+.
- requests
- beautifulsoup4
- playwright
  
#### Setup

1. Clone the repository:
```
git clone https://github.com/DracSec/URLsnap3r.git
cd URLsnap3r
```

2. Install the tool:

```
bash install.sh
```

#### Usage

The tool requires a single positional argument: the full URL of the target website, including the scheme (http:// or https://).

```
./bin/python URLsnap3r.py https://target.com/
```

Example with Specific Path

```
python URList3r.py https://staging.target.com/app/dashboard
```

Output Example
```
🔍 Starting scrape on: https://github.com/dragown
✅ Found 41 unique external JS files.

--- Extracting Links from JS Files ---
  -> Fetching JS: https://github.githubassets.com/assets/github-elements-837d26c249ef0f1d.js
  -> No links found in https://github.githubassets.com/assets/github-elements-837d26c249ef0f1d.js
  -> Fetching JS: https://github.githubassets.com/assets/environment-39e5b412c63ea4f0.js
  -> No links found in https://github.githubassets.com/assets/environment-39e5b412c63ea4f0.js
  -> Fetching JS: https://github.githubassets.com/assets/28839-632d00a964e8dbd5.js
  -> No links found in https://github.githubassets.com/assets/28839-632d00a964e8dbd5.js
  -> Fetching JS: https://github.githubassets.com/assets/79039-9ce5da88e09eef89.js
  -> No links found in https://github.githubassets.com/assets/79039-9ce5da88e09eef89.js

[...]
  
--- Final List of All Extracted Links ---
http://localhost
http://www.w3.org/1998/Math/MathML
http://www.w3.org/1999/xhtml
http://www.w3.org/1999/xlink
http://www.w3.org/2000/svg
http://www.w3.org/XML/1998/namespace
https://github.com
https://github.githubassets.com/$
https://github.githubassets.com/&
https://github.githubassets.com/([^\\/]+)
https://github.githubassets.com/*
https://github.githubassets.com/*!sc*/\n
https://github.githubassets.com/*|*/
https://github.githubassets.com/*|*/}
https://github.githubassets.com/>
https://github.githubassets.com/?([^\\/]+)?
https://github.githubassets.com/assets/react-core-4d91a4784b23bcae.js
...
https://github.githubassets.com/users/settings/security_products/configurations/new
https://react.dev/errors/

Total unique links found: 42

[...]

--- Checking Status and Taking Screenshots (42 links) ---
🌐 Visiting: http://localhost
  -> Error processing http://localhost: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost/
Call log:
  - navigating to "http://localhost/", waiting until "load"
🌐 Visiting: http://www.w3.org/1998/Math/MathML
  -> Error processing http://www.w3.org/1998/Math/MathML: Page.goto: Navigation to "http://www.w3.org/1998/Math/MathML" is interrupted by another navigation to "chrome-error://chromewebdata/"
Call log:
  - navigating to "http://www.w3.org/1998/Math/MathML", waiting until "load"
🌐 Visiting: http://www.w3.org/1999/xhtml
  -> Error processing http://www.w3.org/1999/xhtml: Page.goto: Navigation to "http://www.w3.org/1999/xhtml" is interrupted by another navigation to "https://www.w3.org/1998/Math/MathML/"
Call log:
  - navigating to "http://www.w3.org/1999/xhtml", waiting until "load"
🌐 Visiting: http://www.w3.org/1999/xlink
  -> Error processing http://www.w3.org/1999/xlink: Page.goto: Navigation to "http://www.w3.org/1999/xlink" is interrupted by another navigation to "https://www.w3.org/1999/xhtml/"
Call log:
  - navigating to "http://www.w3.org/1999/xlink", waiting until "load"
🌐 Visiting: http://www.w3.org/2000/svg
...
🌐 Visiting: https://github.githubassets.com/users/settings/security_products/configurations/new
  -> Status: 404 | Saved: github%2Fgithubassets%2Fcom%2Fusers%2Fsettings%2Fsecurity%2Fproducts%2Fconfigurations%2Fnew.png
🌐 Visiting: https://react.dev/errors/
  -> Status: 200 | Saved: react%2Fdev%2Ferrors%2F.png
```

<img width="500" height=auto alt="image" src="https://github.com/user-attachments/assets/9e1470cf-81db-4c3e-b51c-351890eb4c13" />

