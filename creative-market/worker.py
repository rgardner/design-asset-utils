import os

import redis
from rq import Worker, Queue, Connection

LISTEN = ['high', 'default', 'low']
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
CONN = redis.from_url(REDIS_URL)


def main():
    with Connection(CONN):
        worker = Worker(map(Queue, LISTEN))
        worker.work()


if __name__ == '__main__':
    main()
