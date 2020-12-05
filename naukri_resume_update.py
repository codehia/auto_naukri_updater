from os import environ as env
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv, find_dotenv
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoApplyToNaukri(object):
    def __init__(self, geckodriver_path=""):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            options=options, executable_path=geckodriver_path
        )

    def login(self, email, password):
        try:
            self.driver.get("https://www.naukri.com/nlogin/login")
            time.sleep(10)
            email_field = self.driver.find_element_by_xpath('//*[@id="usernameField"]')
            password_field = self.driver.find_element_by_xpath(
                '//*[@id="passwordField"]'
            )
            button = self.driver.find_element_by_xpath(
                '//*[@id="loginForm"]/div[3]/div[3]/div/button[1]'
            )
            email_field.send_keys(email)
            password_field.send_keys(password)
            ActionChains(self.driver).click(button).perform()
        except:
            return False
        try:
            profile_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    By.XPATH,
                    '//*[@id="root"]/div/div/span/div/div/div/div[2]/div/div[2]/div[1]/div/a[1]',
                )
            )
            return True
        except:
            return False

    def update(self, resume_path):
        time.sleep(10)
        profile_page = self.driver.find_elements_by_xpath(
            '//*[@id="root"]/div/div/span/div/div/div/div[2]/div/div[2]/div[1]/div/a[1]'
        )[0].get_attribute("href")
        self.driver.get(profile_page)
        time.sleep(10)
        resume_button = self.driver.find_element_by_xpath('//*[@id="attachCV"]')
        resume_button.send_keys(resume_path)
        time.sleep(10)
        return True

    def destory(self):
        self.driver.quit()


def main(email, password, resume_path, gecko_path):
    auto_apply = AutoApplyToNaukri(gecko_path)
    auto_apply.login(email, password)
    auto_apply.update(resume_path)
    auto_apply.destory()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    email = env.get("EMAIL")
    password = env.get("PASSWORD")
    resume_path = env.get("RESUME_PATH")
    gecko_path = env.get("GECKO_DRIVER_PATH")
    main(email, password, resume_path, gecko_path)
