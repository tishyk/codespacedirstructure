# semaphore_signal.py
#
# An example of using a semaphore to signal

import threading
import time

semaphore = threading.Semaphore(2)
item = []


def producer():
    global item
    print("I'm the producer and I produce data.")
    print("Producer is going to get consumer data.")

    with semaphore:
        item.append("Hello")
        time.sleep(5)
        print("Producer is alive. Signaling the consumer.")


def consumer():
    print("I'm a consumer and I wait for data.")
    semaphore.acquire()
    item.append(threading.currentThread().getName())
    print("Consumer got", item)
    semaphore.release()


t2 = threading.Thread(target=consumer, name='2')
t3 = threading.Thread(target=consumer, name='3')
t4 = threading.Thread(target=consumer, name='4')
t5 = threading.Thread(target=consumer, name='5')

t1 = threading.Thread(target=producer)

t1.start()
t3.start()
t2.start()
t4.start()
t5.start()
