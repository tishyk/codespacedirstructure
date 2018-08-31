# generator.py

def countdown_task(n):
    while n > 0:
        print(n)
        yield n
        n -= 1

# A list of tasks to run
from collections import deque

tasks = deque([countdown_task(5),
               countdown_task(10),
               countdown_task(15)])


def scheduler(tasks):
    while tasks:
        task = tasks.popleft()
        try:
            next(task)  # Run to the next yield
            tasks.append(task)  # Reschedule
        except StopIteration:
            pass


# Run it
scheduler(tasks)
