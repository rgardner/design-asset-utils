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

CHROME_SHIM = os.environ['GOOGLE_CHROME_SHIM']
DEBUG = bool(os.environ['CREATIVE_MARKET_DEBUG'])
FACEBOOK_USERNAME = os.environ['CREATIVE_MARKET_FB_USERNAME']
FACEBOOK_PASSWORD = os.environ['CREATIVE_MARKET_FB_PASSWORD']
LOGGER = logging.getLogger(__name__)


class CreativeMarketError(WebDriverException):
    """Raised when an error occurs syncing the Creative Market free goods.

    Attributes:
        message: str
        page_screenshot: binary
    """

    def __init__(self, msg, driver):
        super().__init__(msg, driver.get_screenshot_as_png())


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CHROME_SHIM
    if not DEBUG:
        chrome_options.add_argument('headless')

    with closing_chrome_driver(chrome_options=chrome_options) as driver:
        try:
            download_free_goods(driver, FACEBOOK_USERNAME, FACEBOOK_PASSWORD)
        except WebDriverException as ex:
            log_error(ex)


def download_free_goods(driver, username, password):
    login(driver, username, password)

    driver.get('https://creativemarket.com/free-goods')
    free_sync_links = get_free_dropbox_sync_links(driver)
    links_to_click = [
        link for link in free_sync_links if link.text == 'Sync to Dropbox'
    ]
    LOGGER.info('%d unclicked sync links found', len(links_to_click))

    for link in links_to_click:
        link.click()
        time.sleep(1)

    LOGGER.info('Successfully downloaded free goods')


def login(driver, username, password):
    """Log in to Creative Market using Facebook."""
    driver.get('https://creativemarket.com/sign-in')
    facebook_sign_in_container = driver.find_element_by_css_selector(
        '#sign-in-facebook > a')
    facebook_sign_in_container.click()

    # Facebook's sign-in page has opened in the background and needs to be
    # switched to
    facebook_sign_in_window = driver.window_handles[-1]
    driver.switch_to_window(facebook_sign_in_window)
    if not driver.current_url.startswith('https://www.facebook.com/login'):
        message = f'unexpected Facebook login url {driver.current_url}'
        raise CreativeMarketError(message, driver)

    login_email_field = driver.find_element_by_css_selector('input[type=text]')
    login_email_field.send_keys(username)
    login_password_field = driver.find_element_by_css_selector(
        'input[type=password]')
    login_password_field.send_keys(password)
    login_button = driver.find_element_by_css_selector('input[value="Log In"]')
    login_button.click()

    # wait for login to complete
    time.sleep(2)

    # switch back to primary window
    driver.switch_to_window(driver.window_handles[0])
    if driver.current_url != 'https://creativemarket.com/':
        message = f'unexpected url after logging in: {driver.current_url}'
        raise CreativeMarketError(message, driver)


def get_free_dropbox_sync_links(driver):
    assert driver.current_url == 'https://creativemarket.com/free-goods'

    dropbox_sync_links = driver.find_elements_by_css_selector('.btn-dropbox')
    return [link for link in dropbox_sync_links if link.is_displayed()]


def log_error(ex: WebDriverException):
    LOGGER.error('Creative Market downloader failed: %s', ex.msg)
    error_screenshot_filename = f'{datetime.utcnow().isoformat()}.png'
    with open(error_screenshot_filename, 'wb') as f:
        f.write(ex.screen)


@contextmanager
def closing_chrome_driver(*args, **kwargs):
    driver = webdriver.Chrome(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.close()


if __name__ == '__main__':
    main()
