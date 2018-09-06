import pytest

import clock
import checker


def test_end_to_end():
    clock.scheduled_download().check_returncode()
    assert checker.has_download_succeeded()
    clock.scheduled_check().check_returncode()


@pytest.mark.email
def test_error_notifier():
    checker.notify_download_failed()
