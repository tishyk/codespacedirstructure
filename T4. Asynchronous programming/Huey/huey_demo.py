"""
huey is:

a task queue (2019-04-01: version 2.0 released)
written in python (2.7+, 3.4+)
clean and simple API
redis, sqlite, or in-memory storage

huey supports:

multi-process, multi-thread or greenlet task execution models
schedule tasks to execute at a given time, or after a given delay
schedule recurring tasks, like a crontab
automatically retry tasks that fail
task prioritization
task result storage
task locking
task pipelines and chains
"""

from huey import crontab, Huey, BlackHoleHuey, MemoryHuey, SqliteHuey, RedisExpireHuey, PriorityRedisHuey, RedisHuey
import time

huey = MemoryHuey('my-app')

def generate_nightly_report():
    print('Generate report')

def crontab(**kwargs):
    period = kwargs.get('hour', 0)*3600 + \
             kwargs.get('minute', 0)*60 + \
             kwargs.get('seconds', 0)
    while True:
        time.sleep(period)
        yield True


@huey.task()
def add_numbers(a, b):
    return a + b

@huey.periodic_task(crontab(minute=0, hour=2))
def nightly_report():
    generate_nightly_report()
