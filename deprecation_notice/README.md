# Add Deprecation Notice to README on IBMCOM

## Setup

1. Download [chromedriver](https://sites.google.com/chromium.org/driver/) for Google Chrome/Chromium based browsers
2. Create a virtual environment for Python: `python -m venv venv`
3. Activate the virtual environment: `.\venv\Scripts\activate`
4. Modify the template `README.mustache` with [mustache](https://mustache.github.io/) templating (if required)

## Usage
1. Run the script `python ra_main.py`
2. Enter Docker Hub **Username** as well as **Password** as prompted
3. Enter the Absolute Browser path for Chromium-based browsers like _Edge, Brave_. Enter nothing if using _Google Chrome_
4. Enter Input CSV file path if we need to update specific READMEs, empty if we need to update all
