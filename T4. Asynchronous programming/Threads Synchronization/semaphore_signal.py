# semaphore_signal.py
#
# An example of using a semaphore to signal

import threading
import time

done = threading.Semaphore(0)
item = None


def producer():
    global item
    print("I'm the producer and I produce data.")
    print("Producer is going to sleep.")
    time.sleep(5)
    item = "Hello"
    print("Producer is alive. Signaling the consumer.")
    done.release()


def consumer():
    print("I'm a consumer and I wait for data.")
    print("Consumer is waiting.")
    done.acquire()
    print("Consumer got", item)


t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
