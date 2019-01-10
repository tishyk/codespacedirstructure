from multiprocessing import Pool
import string
import time
import threading

def func(n):
    time.sleep(n)
    print(threading.current_thread().name)
    return 'i was d this task during %i seconds'%n

if __name__ == "__main__":
    p = Pool(processes=3)
    result = p.map(func, (0,15,4,8,9,4,2,3))
    for n in result:
        print(n)