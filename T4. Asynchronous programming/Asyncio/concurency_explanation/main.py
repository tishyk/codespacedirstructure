import time
from math import sqrt
from queue import deque


def fibonacci():
    yield 2
    a = 2
    b = 1
    while True:
        yield b
        a, b = b, a + b


def search(iterable, predicate):
    """ Return the first item satisfying a predicate """
    for item in iterable:
        if predicate(item):
            return item
    raise ValueError('Not found')


def async_search(iterable, predicate):
    for item in iterable:
        if predicate(item):
            return item
        yield
    raise ValueError('Not found')


class Task:
    """ Aggregates a coroutine and integer id """
    next_id = 0

    def __init__(self, routine):
        self.id = Task.next_id
        Task.next_id += 1
        self.routine = routine


class Scheduler:
    def __init__(self):
        self.executable_tasks = deque()
        self.completed_task_results = {}
        self.failed_task_error = {}

    def add(self, routine):
        task = Task(routine)
        self.executable_tasks.append(task)
        return task.id

    def run_until_complete(self):
        while len(self.executable_tasks) != 0:
            task = self.executable_tasks.popleft()
            print("Running task {} ... ".format(task.id), end='')
            try:
                yielded = next(task.routine)
            except StopIteration as stopped:
                print("completed with result: {!r}".format(stopped.value))
                self.completed_task_results[task.id] = stopped.value
            except Exception as exec:
                print("failed with exception: {}".format(exec))
            else:
                assert yielded is None
                print('now yielded')
                self.executable_tasks.append(task)


scheduler = Scheduler()


# scheduler.add(async_search(fibonacci(), lambda x: len(str(x))>=6))
# scheduler.add(async_search(fibonacci(), lambda x: len(str(x))>=9))
# scheduler.run_until_complete()

# print(scheduler.completed_task_results[0])
# print(scheduler.completed_task_results[1])


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x) + 1)):
        if x % i == 0:
            return False
    return True


def async_print_matches(iterable, predicate):
    "Similar to async_search, but prints all matches"

    for item in iterable:
        if predicate(item):
            print("Found: ", item, end=', ')
        yield


scheduler = Scheduler()


# scheduler.add(async_print_matches(fibonacci(), is_prime))
# scheduler.run_until_complete()

def repetitive_msg(msg, interval_seconds):
    while True:
        print(msg)
        start = time.time()
        expiry = start + interval_seconds
        while True:
            now = time.time()
            if now >= expiry:
                break


def async_repetitive_msg(msg, interval_seconds):
    while True:
        print(msg)
        start = time.time()
        expiry = start + interval_seconds
        while True:
            yield  # Ensure coroutine always yield at least once
            now = time.time()
            if now >= expiry:
                break


scheduler = Scheduler()


# scheduler.add(async_print_matches(fibonacci(), is_prime))
# scheduler.add(async_repetitive_msg('Interval message', 2))
# scheduler.run_until_complete()

def async_is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x) + 1)):
        if x % i == 0:
            return False
        yield from async_sleep(0)
    return True


def async_search(iterable, predicate):
    for item in iterable:
        if predicate(item):
            return item
        yield from async_sleep(0)
    raise ValueError('Not found')


def async_print_matches(iterable, async_predicate):
    for item in iterable:
        matches = yield from async_predicate(item)
        if async_predicate(item):
            print("Found: ", item, end=', ')


def async_repetitive_msg(msg, interval):
    while True:
        print(msg)
        yield from async_sleep(interval)


def async_sleep(interval):
    start = time.time()
    expiry = start + interval
    while True:
        yield
        now = time.time()
        if now >= expiry:
            break


scheduler = Scheduler()
# scheduler.add(async_repetitive_msg('Interval message', 2))
# scheduler.add(async_print_matches(fibonacci(), async_is_prime))
# scheduler.run_until_complete()
