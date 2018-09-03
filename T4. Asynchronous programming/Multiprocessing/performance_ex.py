# perfmp.py
#
# A performance test with processes

import time
import multiprocessing


def count(n):
    while n > 0:
        n -= 1


start = time.time()
count(10000000)
count(10000000)
end = time.time()
print("Sequential", end - start)

start = time.time()
p1 = multiprocessing.Process(target=count, args=(10000000,))
p2 = multiprocessing.Process(target=count, args=(10000000,))

if __name__ == "__main__": # remove statement for test
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print("Multiprocessing", end - start)
