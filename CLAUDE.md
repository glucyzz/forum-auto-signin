# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Code Architecture and Structure
This repository contains a Python script (`main.py`) designed for automating forum sign-in. It utilizes `selenium` with `undetected-chromedriver` to interact with web pages, bypassing bot detection. The script can log in using either username/password or pre-provided cookies. After successful login, it attempts to click a sign-in icon and a "lucky draw" button (e.g., "试试手气" or "鸡腿 x 5").

Key components:
- `main.py`: The main script that orchestrates the automation.
    - `click_sign_icon(driver, ns_random)`: A function that handles the clicking of the sign-in icon and a subsequent button.
    - `main()`: The entry point of the script, responsible for browser initialization, login (via cookies or credentials), and calling `click_sign_icon`.
- `requirements.txt`: Lists Python dependencies, including `selenium`, `undetected-chromedriver`, `requests`, `curl_cffi`, `beautifulsoup4`, and `webdriver_manager`.
- `node_modules/`: Suggests the presence of Node.js dependencies, although no explicit Node.js script was found in the initial `ls` output.

## Configuration
The script's behavior is heavily influenced by environment variables:
- `FORUM_URL`: The login URL of the target forum.
- `FORUM_USERNAME`: Username for login.
- `FORUM_PASSWORD`: Password for login.
- `FORUM_COOKIES`: Optional JSON string of cookies for cookie-based login.
- `USERNAME_SELECTOR`: CSS selector for the username input field.
- `PASSWORD_SELECTOR`: CSS selector for the password input field.
- `LOGIN_BUTTON_SELECTOR`: CSS selector for the login button.
- `SIGN_ICON_XPATH`: XPath for the sign-in icon.
- `LUCKY_BUTTON_XPATH`: XPath for the "试试手气" button.
- `CHICKEN_BUTTON_XPATH`: XPath for the "鸡腿 x 5" button.
- `NS_RANDOM`: Boolean flag to determine which "lucky draw" button to click.

## Common Development Tasks

### Running the script
The script can be run directly using Python:
```bash
python forum-auto-signin/main.py
```

Before running, ensure all Python dependencies are installed:
```bash
pip install -r forum-auto-signin/requirements.txt
```

And configure the necessary environment variables (e.g., `FORUM_URL`, `FORUM_USERNAME`, `FORUM_PASSWORD`, etc.) according to the target forum. For example:
```bash
export FORUM_URL='https://example.com/login'
export FORUM_USERNAME='your_username'
export FORUM_PASSWORD='your_password'
python forum-auto-signin/main.py
```
