from contextlib import contextmanager
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROME_SHIM = os.environ['GOOGLE_CHROME_SHIM']


class CreativeMarketError(WebDriverException):
    """Raised when an error occurs syncing the Creative Market free goods."""

    def __init__(self, msg: str, driver) -> None:
        super().__init__(msg, driver.get_screenshot_as_png())


class CreativeMarketDriver:
    def __init__(self, headless=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = CHROME_SHIM
        if headless:
            chrome_options.add_argument('headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def login(self, username, password):
        """Log in to Creative Market using a Creative Market account."""
        self.driver.get('https://creativemarket.com/sign-in')

        login_username_field = self.driver.find_element_by_id('input-username')
        login_username_field.send_keys(username)
        login_password_field = self.driver.find_element_by_id('input-password')
        login_password_field.send_keys(password)
        login_button = self.driver.find_element_by_css_selector(
            '#sign-in-form > button')
        login_button.click()

        # wait for login to complete
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'user-name')))

    def get_free_dropbox_sync_links(self):
        self.driver.get('https://creativemarket.com/free-goods')
        dropbox_sync_links = self.driver.find_elements_by_css_selector(
            '.btn-dropbox')
        return [link for link in dropbox_sync_links if link.is_displayed()]

    def get_screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    def quit(self):
        self.driver.quit()


@contextmanager
def quitting_creative_market_driver(headless=True):
    driver = CreativeMarketDriver(headless)
    try:
        yield driver
    finally:
        driver.quit()
