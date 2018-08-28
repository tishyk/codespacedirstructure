import time
from random import randint
import threading

queue = []


def producer():
    for i in range(0, 6):
        time.sleep(0.5)
        queue.append(randint(0, 9))


def consumer():
    while True:
        if len(queue) > 0:
            print(queue)
        if len(queue)==6:
            break


if __name__ == "__main__":
    p = threading.Thread(target=producer, args=())
    c = threading.Thread(target=consumer, args=())
    p.start()
    c.start()
