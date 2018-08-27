from contextlib import contextmanager
import os

import requests
from selenium import webdriver

import downloader

MAILGUN_SEND_URL = os.environ['CREATIVE_MARKET_MAILGUN_URL']
MAILGUN_API_KEY = os.environ['CREATIVE_MARKET_MAILGUN_API_KEY']
MAILGUN_FROM = os.environ['CREATIVE_MARKET_MAILGUN_FROM']
NOTIFY_TO_EMAIL_ADDRESS = os.environ['CREATIVE_MARKET_NOTIFY_TO_EMAIL_ADDRESS']


def main():
    if not has_download_succeeded():
        notify_download_failed()


def has_download_succeeded():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    with downloader.closing_chrome_driver(
            chrome_options=chrome_options,
            executable_path=downloader.CHROME_DRIVER_EXE_ABS_PATH) as driver:
        downloader.download_free_goods(driver, downloader.FACEBOOK_USERNAME,
                                       downloader.FACEBOOK_PASSWORD)
        free_sync_links = downloader.get_free_dropbox_sync_links(driver)
        return all(link.text == 'Synced' for link in free_sync_links)


def notify_download_failed():
    response = requests.post(
        MAILGUN_SEND_URL,
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': MAILGUN_FROM,
            'to': NOTIFY_TO_EMAIL_ADDRESS,
            'subject': 'Creative Market Free Good Downloader Failed',
            'text': 'This message is sent from an unmonitored account.',
        })


if __name__ == '__main__':
    main()
