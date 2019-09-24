from collections import deque


def countdown_task(n):
    while n > 0:
        print(n)
        yield n
        n -= 1

# A list of tasks to run
tasks = deque([countdown_task(5),
               countdown_task(7),
               countdown_task(9)])


def scheduler(tasks):
    while tasks:
        task = tasks.popleft()
        try:
            next(task)
            tasks.append(task)
        except StopIteration:
            pass


scheduler(tasks)
