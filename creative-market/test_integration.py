import time

import pytest

import clock
import checker


def test_end_to_end():
    clock.scheduled_download()
    assert checker.has_download_succeeded()
    clock.scheduled_check()


@pytest.mark.email
def test_error_notifier():
    checker.notify_download_failed()
