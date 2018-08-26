#!/usr/bin/env python3
"""
usage: downloader.py

Tool to automatically download the free goods each week from creativemarket.com
"""

from contextlib import contextmanager
import os
import time

from selenium import webdriver

CHROME_DRIVER_EXE_ABS_PATH = os.environ['CREATIVE_MARKET_CHROME_DRIVER']
FACEBOOK_USERNAME = os.environ['CREATIVE_MARKET_FB_USERNAME']
FACEBOOK_PASSWORD = os.environ['CREATIVE_MARKET_FB_PASSWORD']


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    with closing_chrome_driver(
            chrome_options=chrome_options,
            executable_path=CHROME_DRIVER_EXE_ABS_PATH) as driver:
        # Sign in via Facebook
        driver.get('https://creativemarket.com/sign-in')
        facebook_sign_in_container = driver.find_element_by_css_selector(
            '#sign-in-facebook > a')
        facebook_sign_in_container.click()

        # Facebook's sign-in page has opened in the background and needs to be
        # switched to
        facebook_sign_in_window = driver.window_handles[-1]
        driver.switch_to_window(facebook_sign_in_window)

        login_email_field = driver.find_element_by_css_selector(
            'input[type=text]')
        login_email_field.send_keys(FACEBOOK_USERNAME)
        login_password_field = driver.find_element_by_css_selector(
            'input[type=password]')
        login_password_field.send_keys(FACEBOOK_PASSWORD)
        login = driver.find_element_by_css_selector('input[value="Log In"]')
        login.click()

        # wait for login to complete
        time.sleep(0.5)

        # switch back to primary window
        driver.switch_to_window(driver.window_handles[0])

        driver.get('https://creativemarket.com/free-goods')
        dropbox_sync_links = driver.find_elements_by_css_selector(
            '.btn-dropbox')
        for link in dropbox_sync_links:
            # Filter out hidden links for premium goods that we don't have
            # access to
            if link.is_displayed():
                link.click()
                time.sleep(0.2)


@contextmanager
def closing_chrome_driver(*args, **kwargs):
    driver = webdriver.Chrome(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.close()


if __name__ == '__main__':
    main()
