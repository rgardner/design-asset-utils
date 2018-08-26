#!/usr/bin/env python3
"""
usage: downloader.py

Tool to automatically download the free goods each week from creativemarket.com
"""

from contextlib import contextmanager
from datetime import datetime
import logging
import os
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

CHROME_DRIVER_EXE_ABS_PATH = os.environ['CREATIVE_MARKET_CHROME_DRIVER']
DEBUG = bool(os.environ['CREATIVE_MARKET_DEBUG'])
FACEBOOK_USERNAME = os.environ['CREATIVE_MARKET_FB_USERNAME']
FACEBOOK_PASSWORD = os.environ['CREATIVE_MARKET_FB_PASSWORD']

LOGGER = logging.getLogger(__name__)


class CreativeMarketError(Exception):
    """Raised when an error occurs syncing the Creative Market free goods.

    Attributes:
        page_screenshot: binary
    """

    def __init__(self, *, driver=None, web_driver_exception=None):
        super().__init__()

        if (driver is not None) and (web_driver_exception is not None):
            raise ValueError(
                'Only one of driver, web_driver_exception expected')

        if web_driver_exception is not None:
            self.page_screenshot = web_driver_exception.screen
        else:
            self.page_screenshot = driver.get_screenshot_as_png()


def main():
    chrome_options = webdriver.ChromeOptions()
    if not DEBUG:
        chrome_options.add_argument('headless')

    with closing_chrome_driver(
            chrome_options=chrome_options,
            executable_path=CHROME_DRIVER_EXE_ABS_PATH) as driver:
        try:
            login(driver, FACEBOOK_USERNAME, FACEBOOK_PASSWORD)

            driver.get('https://creativemarket.com/free-goods')
            dropbox_sync_links = driver.find_elements_by_css_selector(
                '.btn-dropbox')
            for link in dropbox_sync_links:
                # Filter out hidden links for premium goods that we don't have
                # access to
                if link.is_displayed():
                    link.click()
                    time.sleep(0.2)

        except CreativeMarketError as ex:
            LOGGER.error('Creative Market downloader failed')
            error_screenshot_filename = f'{datetime.utcnow().isoformat()}.png'
            with open(error_screenshot_filename, 'wb') as f:
                f.write(ex.page_screenshot)


def login(driver, username, password):
    """Log in to Creative Market using Facebook."""
    try:
        driver.get('https://creativemarket.com/sign-in')
        facebook_sign_in_container = driver.find_element_by_css_selector(
            '#sign-in-facebook > a')
        facebook_sign_in_container.click()

        # Facebook's sign-in page has opened in the background and needs to be
        # switched to
        facebook_sign_in_window = driver.window_handles[-1]
        driver.switch_to_window(facebook_sign_in_window)
        if not driver.current_url.startswith('https://www.facebook.com/login'):
            raise CreativeMarketError(driver=driver)

        login_email_field = driver.find_element_by_css_selector(
            'input[type=text]')
        login_email_field.send_keys(username)
        login_password_field = driver.find_element_by_css_selector(
            'input[type=password]')
        login_password_field.send_keys(password)
        login_button = driver.find_element_by_css_selector(
            'input[value="Log In"]')
        login_button.click()

        # wait for login to complete
        time.sleep(1)

        # switch back to primary window
        driver.switch_to_window(driver.window_handles[0])
        if driver.current_url != 'https://creativemarket.com/':
            raise CreativeMarketError(driver=driver)

    except WebDriverException as ex:
        raise CreativeMarketError(web_driver_exception=ex) from ex


@contextmanager
def closing_chrome_driver(*args, **kwargs):
    driver = webdriver.Chrome(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.close()


if __name__ == '__main__':
    main()
