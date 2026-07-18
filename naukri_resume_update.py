import logging
import os
import time
from os import environ as env
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


class NaukriResumeUpdater:
    def __init__(self, gecko_path, profile_path=None, headless=False, binary_path=None):
        log.info("Launching Firefox (headless=%s)", headless)
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
        log.info("Firefox started")

    def _dump_failure(self, label):
        ts = int(time.time())
        shot_path = f"/tmp/naukri_fail_{label}_{ts}.png"
        src_path = f"/tmp/naukri_fail_{label}_{ts}.html"
        try:
            self.driver.save_screenshot(shot_path)
            log.info("Screenshot saved: %s", shot_path)
        except Exception as e:
            log.warning("Could not save screenshot: %s", e)
        try:
            with open(src_path, "w") as f:
                f.write(self.driver.page_source)
            log.info("Page source saved: %s", src_path)
        except Exception as e:
            log.warning("Could not save page source: %s", e)

    def update_resume(self, resume_path):
        url = "https://www.naukri.com/mnjuser/profile"
        log.info("Navigating to %s", url)
        self.driver.get(url)
        log.info("Current URL: %s | Title: %s", self.driver.current_url, self.driver.title)

        log.info("Waiting for resume file input (#resume)")
        try:
            resume_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "resume"))
            )
        except Exception:
            log.error("Timed out waiting for #resume — URL: %s | Title: %s", self.driver.current_url, self.driver.title)
            self._dump_failure("resume_input")
            raise

        log.info("Found #resume, sending resume path: %s", resume_path)
        resume_input.send_keys(resume_path)

        # Confirmation: resume card in #profile-section-resume re-renders with
        # an "Uploaded today" caption once the upload lands. Must use contains(., ...)
        # not contains(text(), ...): React splits the caption into two text nodes
        # ("Uploaded " + "today"), and text() only tests the first one.
        confirmation_xpath = (
            "//div[@id='profile-section-resume']"
            "//p[contains(., 'Uploaded today')]"
        )
        log.info("Waiting for upload confirmation ('Uploaded today' in #profile-section-resume)")
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, confirmation_xpath))
            )
        except Exception:
            log.error("Timed out waiting for 'Uploaded today' confirmation")
            log.error("URL at failure: %s | Title: %s", self.driver.current_url, self.driver.title)
            self._dump_failure("confirmation")
            raise

        log.info("Upload confirmed: resume card shows 'Uploaded today'")

    def destroy(self):
        log.info("Closing browser")
        self.driver.quit()


def main(resume_path, gecko_path, profile_path=None, headless=False, binary_path=None):
    log.info(
        "Starting update | resume=%s gecko=%s profile=%s headless=%s binary=%s",
        resume_path, gecko_path, profile_path, headless, binary_path,
    )
    updater = NaukriResumeUpdater(gecko_path, profile_path=profile_path, headless=headless, binary_path=binary_path)
    try:
        updater.update_resume(resume_path)
        log.info("Resume update complete")
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
