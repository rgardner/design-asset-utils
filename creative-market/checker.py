#!/usr/bin/env python3
"""
usage: ./checker.py

Tool to check if download succeeded, and if not, send a notification email.
"""

import logging
import os
import sys

import requests

import creative_market

DEBUG = bool(os.environ['CREATIVE_MARKET_DEBUG'])
FACEBOOK_USERNAME = os.environ['CREATIVE_MARKET_FB_USERNAME']
FACEBOOK_PASSWORD = os.environ['CREATIVE_MARKET_FB_PASSWORD']
MAILGUN_SEND_URL = os.environ['CREATIVE_MARKET_MAILGUN_URL']
MAILGUN_API_KEY = os.environ['CREATIVE_MARKET_MAILGUN_API_KEY']
MAILGUN_FROM = os.environ['CREATIVE_MARKET_MAILGUN_FROM']
NOTIFY_TO_EMAIL_ADDRESS = os.environ['CREATIVE_MARKET_NOTIFY_TO_EMAIL_ADDRESS']

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main(argv=None):
    if not has_download_succeeded() and argv and '--send-email-on-error' in argv:
        notify_download_failed()


def has_download_succeeded():
    with creative_market.chrome_driver(DEBUG) as driver:
        creative_market.login(driver, FACEBOOK_USERNAME, FACEBOOK_PASSWORD)

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
    main(sys.argv)
