from datetime import datetime

from selenium import webdriver

import downloader


def test_login():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    with downloader.closing_chrome_driver(
            chrome_options=chrome_options,
            executable_path=downloader.CHROME_DRIVER_EXE_ABS_PATH) as driver:

        try:
            downloader.login(driver, downloader.FACEBOOK_USERNAME,
                             downloader.FACEBOOK_PASSWORD)

        except downloader.CreativeMarketError as ex:
            error_screenshot_filename = f'{datetime.utcnow().isoformat()}.png'
            with open(error_screenshot_filename, 'wb') as f:
                f.write(ex.page_screenshot)

            raise ex


def test_downloader():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    with downloader.closing_chrome_driver(
            chrome_options=chrome_options,
            executable_path=downloader.CHROME_DRIVER_EXE_ABS_PATH) as driver:
        downloader.download_free_goods(driver, downloader.FACEBOOK_USERNAME,
                                       downloader.FACEBOOK_PASSWORD)
        free_sync_links = downloader.get_free_dropbox_sync_links(driver)
        for link in free_sync_links:
            assert link.text == 'Synced'
