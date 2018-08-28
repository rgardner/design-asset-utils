#!/usr/bin/env python3
"""
usage: ./checker.py

Tool to check if download succeeded, and if not, send a notification email.
"""

import os

import requests

import creative_market

MAILGUN_SEND_URL = os.environ['CREATIVE_MARKET_MAILGUN_URL']
MAILGUN_API_KEY = os.environ['CREATIVE_MARKET_MAILGUN_API_KEY']
MAILGUN_FROM = os.environ['CREATIVE_MARKET_MAILGUN_FROM']
NOTIFY_TO_EMAIL_ADDRESS = os.environ['CREATIVE_MARKET_NOTIFY_TO_EMAIL_ADDRESS']


def main():
    if not has_download_succeeded():
        notify_download_failed()


def has_download_succeeded():
    with creative_market.chrome_driver(CHROME_SHIM, DEBUG) as driver:
        creative_market.login(driver, username, password)

        driver.get('https://creativemarket.com/free-goods')
        free_sync_links = creative_market.get_free_dropbox_sync_links(driver)
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
