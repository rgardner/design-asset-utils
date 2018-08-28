import time

import pytest

import checker
import clock
import downloader


def test_end_to_end():
    downloader.main()
    assert checker.has_download_succeeded()
    checker.main()


@pytest.mark.redis_queue
def test_end_to_end_redis_queue():
    clock.scheduled_download()
    time.sleep(2)
    assert checker.has_download_succeeded()
    clock.scheduled_check()


@pytest.mark.email
def test_error_notifier():
    checker.notify_download_failed()
