from os import environ as env
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv


class NaukriResumeUpdater:
    def __init__(self, gecko_path, profile_path=None, headless=False, binary_path=None):
        options = Options()
        if headless:
            options.add_argument("-headless")
        if profile_path:
            options.add_argument("-profile")
            options.add_argument(profile_path)
        if binary_path:
            options.binary_location = binary_path
        service = Service(executable_path=gecko_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)

    def update_resume(self, resume_path):
        self.driver.get("https://www.naukri.com/mnjuser/profile")
        resume_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "attachCV"))
        )
        resume_input.send_keys(resume_path)
        self.wait.until(
            lambda d: d.find_element(By.ID, "attachCVMsgBox").text.strip()
        )

    def destroy(self):
        self.driver.quit()


def main(resume_path, gecko_path, profile_path=None, headless=False, binary_path=None):
    updater = NaukriResumeUpdater(gecko_path, profile_path=profile_path, headless=headless, binary_path=binary_path)
    try:
        updater.update_resume(resume_path)
    finally:
        updater.destroy()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    resume_path = env.get("RESUME_PATH")
    gecko_path = env.get("GECKO_DRIVER_PATH")
    profile_path = env.get("FIREFOX_PROFILE_PATH")
    headless = env.get("HEADLESS", "false").lower() == "true"
    binary_path = env.get("FIREFOX_BINARY_PATH")
    main(resume_path, gecko_path, profile_path=profile_path, headless=headless, binary_path=binary_path)
