# auto_naukri_updater

Uses selenium to open and update your resume to naukri.com
can be added to a cronjob on a daily basis to increase your profile view

# Installation
`pip install -r requirements.txt`
- download and extract geckodriver
- create a .env file in the code folder and add the folowing details to it
```
EMAIL="your_email"
PASSWORD="your_password"
RESUME_PATH="full_path_of_your_resume"
GECKO_DRIVER_PATH="path_to_the_extracted_geckodriver"
```
`python naukri_resume_update.py`
