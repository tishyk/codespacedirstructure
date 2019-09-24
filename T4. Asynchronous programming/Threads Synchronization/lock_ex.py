# lock_ex.py
# A simple example of using a mutex lock for critical sections

import threading
from threading import Lock, Thread

x = 0  # A shared value
x_lock = Lock()  # A lock for synchronizing access to x

COUNT = 1000000


def foo():
    global x
    for i in range(COUNT):
        x_lock.acquire()
        x += 1
        x_lock.release()


def bar():
    global x
    for i in range(COUNT):
        with x_lock:
            x -= 1


t1 = Thread(target=foo)
t2 = Thread(target=bar)
t1.start()
t2.start()
t1.join()
t2.join()
print(x)
