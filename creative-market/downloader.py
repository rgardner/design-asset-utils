#!/usr/bin/env python3
"""
usage: downloader.py

Tool to automatically download the free goods each week from creativemarket.com
"""

from datetime import datetime
import logging
import os
import time

from selenium.common.exceptions import WebDriverException

import creative_market

CHROME_SHIM = os.environ['GOOGLE_CHROME_SHIM']
DEBUG = bool(os.environ['CREATIVE_MARKET_DEBUG'])
FACEBOOK_USERNAME = os.environ['CREATIVE_MARKET_FB_USERNAME']
FACEBOOK_PASSWORD = os.environ['CREATIVE_MARKET_FB_PASSWORD']
LOGGER = logging.getLogger(__name__)


def main():
    with creative_market.chrome_driver(CHROME_SHIM, DEBUG) as driver:
        try:
            download_free_goods(driver, FACEBOOK_USERNAME, FACEBOOK_PASSWORD)
        except WebDriverException as ex:
            log_error(ex)


def download_free_goods(driver, username, password):
    creative_market.login(driver, username, password)

    driver.get('https://creativemarket.com/free-goods')
    free_sync_links = creative_market.get_free_dropbox_sync_links(driver)
    links_to_click = [
        link for link in free_sync_links if link.text == 'Sync to Dropbox'
    ]
    LOGGER.info('%d unclicked sync links found', len(links_to_click))

    for link in links_to_click:
        link.click()
        time.sleep(1)

    LOGGER.info('Successfully downloaded free goods')


def log_error(ex: WebDriverException):
    LOGGER.error('Creative Market downloader failed: %s', ex.msg)
    error_screenshot_filename = f'{datetime.utcnow().isoformat()}.png'
    with open(error_screenshot_filename, 'wb') as f:
        f.write(ex.screen)


if __name__ == '__main__':
    main()
