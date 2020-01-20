# pc_queue.py
#
# An example of using queues to set up producer/consumer problems

import threading
import time
import queue
from threading import  Lock

# A queue of items being produced

items = queue.deque()
lock = Lock()

# A producer thread
def producer():
    print("I'm the producer")
    for i in range(30):
        items.appendleft(i)
    time.sleep(0.5)



# A consumer thread
def consumer():
    print("I'm a consumer", threading.currentThread().name)
    while True:
        try:
            x = items.popleft() # items.pop()
            with lock:
                print(threading.currentThread().name, "got", x)
        except IndexError:
            pass
            # pass print(threading.currentThread().name, "got nothing")



# Launch a bunch of consumers
consumers = [threading.Thread(target=consumer) for i in range(10)]
for c in consumers:
    c.setDaemon(True)
    c.start()

# Run the producer
producer()
