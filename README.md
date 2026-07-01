# auto_naukri_updater

Uses Selenium to re-upload your resume to naukri.com, bumping the "last updated" timestamp. Designed to run as a daily cron job.

## Requirements

- Python 3.13+
- Poetry
- Firefox
- geckodriver (must match your CPU architecture — download from [github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases))

## Installation

```bash
poetry install
```

## Setup

### 1. Firefox profile with Google login

This script authenticates via a Firefox profile that already has your Google account logged in. One-time setup:

1. Open Firefox with a dedicated profile
2. Log into Google in that profile
3. Note the profile directory path

### 2. `.env` file

Create `.env` in the repo root:

```
RESUME_PATH="full_path_to_your_resume"
GECKO_DRIVER_PATH="path_to_geckodriver"
FIREFOX_BINARY_PATH="path_to_firefox_binary"
FIREFOX_PROFILE_PATH="path_to_firefox_profile_directory"
HEADLESS="true"
```

## Run

```bash
poetry run python naukri_resume_update.py
```

## Cron (Debian/Ubuntu)

```bash
crontab -e
```

Add:
```
0 9 * * * cd /path/to/auto_naukri_updater && .venv/bin/python naukri_resume_update.py >> /home/user/naukri.log 2>&1
```

If running headless without a display, use `xvfb-run`:
```
0 9 * * * cd /path/to/auto_naukri_updater && xvfb-run .venv/bin/python naukri_resume_update.py >> /home/user/naukri.log 2>&1
```
