import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

import checker
import downloader
from worker import CONN

JOB_QUEUE = Queue(connection=CONN)
SCHEDULER = BlockingScheduler()


@SCHEDULER.scheduled_job('cron', day_of_week='mon', hour=17)
def scheduled_download():
    print('Scheduling downloader...')
    JOB_QUEUE.enqueue(downloader.main)


@SCHEDULER.scheduled_job('cron', day_of_week='mon', hour=17, minute=15)
def scheduled_check():
    print('Scheduling checker...')
    JOB_QUEUE.enqueue(checker.main, ['--send-email-on-error'])


def main():
    SCHEDULER.start()


if __name__ == '__main__':
    main()
