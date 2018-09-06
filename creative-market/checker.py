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
CREATIVE_MARKET_USERNAME = os.environ['CREATIVE_MARKET_USERNAME']
CREATIVE_MARKET_PASSWORD = os.environ['CREATIVE_MARKET_PASSWORD']
MAILGUN_SEND_URL = os.environ['CREATIVE_MARKET_MAILGUN_URL']
MAILGUN_API_KEY = os.environ['CREATIVE_MARKET_MAILGUN_API_KEY']
MAILGUN_FROM = os.environ['CREATIVE_MARKET_MAILGUN_FROM']
NOTIFY_TO_EMAIL_ADDRESS = os.environ['CREATIVE_MARKET_NOTIFY_TO_EMAIL_ADDRESS']

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    if not has_download_succeeded() and '--send-email-on-error' in sys.argv:
        notify_download_failed()


def has_download_succeeded():
    with creative_market.quitting_creative_market_driver(DEBUG) as driver:
        driver.login(CREATIVE_MARKET_USERNAME, CREATIVE_MARKET_PASSWORD)
        free_sync_links = driver.get_free_dropbox_sync_links()
        return all(link.text == 'Synced' for link in free_sync_links)


def notify_download_failed():
    requests.post(
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
