# perf.py
#
# A performance problem with threads

import time
import threading


def count(n):
    while n > 0:
        n -= 1


start = time.time()
count(10000000)
count(10000000)
end = time.time()
print("Sequential", end - start)

start = time.time()
t1 = threading.Thread(target=count, args=(10000000,))
t2 = threading.Thread(target=count, args=(10000000,))
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print("Threaded", end - start)
