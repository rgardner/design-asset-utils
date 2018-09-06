import os
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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
        """Log in to Creative Market using Facebook."""
        self.driver.get('https://creativemarket.com/sign-in')
        facebook_sign_in_container = self.driver.find_element_by_css_selector(
            '#sign-in-facebook > a')
        facebook_sign_in_container.click()

        # Facebook's sign-in page has opened in the background and needs to be
        # switched to
        facebook_sign_in_window = self.driver.window_handles[-1]
        self.driver.switch_to_window(facebook_sign_in_window)
        if not self.driver.current_url.startswith(
                'https://www.facebook.com/login'):
            message = f'unexpected Facebook login url {self.driver.current_url}'
            raise CreativeMarketError(message, self.driver)

        login_email_field = self.driver.find_element_by_css_selector(
            'input[type=text]')
        login_email_field.send_keys(username)
        login_password_field = self.driver.find_element_by_css_selector(
            'input[type=password]')
        login_password_field.send_keys(password)
        login_button = self.driver.find_element_by_css_selector(
            'input[value="Log In"]')
        login_button.click()

        # wait for login to complete
        time.sleep(2)

        # switch back to primary window
        self.driver.switch_to_window(self.driver.window_handles[0])

    def get_free_dropbox_sync_links(self):
        self.driver.get('https://creativemarket.com/free-goods')
        dropbox_sync_links = self.driver.find_elements_by_css_selector(
            '.btn-dropbox')
        return [link for link in dropbox_sync_links if link.is_displayed()]

    def quit(self):
        self.driver.quit()
