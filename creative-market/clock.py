import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

SCHEDULER = BlockingScheduler()


@SCHEDULER.scheduled_job('cron', day_of_week='mon', hour=17)
def scheduled_download():
    print('Scheduling downloader...')
    subprocess.run(['python3', 'downloader.py'])


@SCHEDULER.scheduled_job('cron', day_of_week='mon', hour=17, minute=15)
def scheduled_check():
    print('Scheduling checker...')
    subprocess.run(['python3', 'checker.py', '--send-email-on-error'])


def main():
    SCHEDULER.start()


if __name__ == '__main__':
    main()
