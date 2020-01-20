# event_barrier.py
#
# An example of using an event to set up a barrier synchronization

import threading
import time

event = threading.Event()

def worker():
    event.wait()  # Wait until initialized
    print("Start.I'm worker", threading.currentThread().name)
    event.clear()
    event.wait()
    print("End.I'm worker", threading.currentThread().name)

def worker2():
    print("Start. I'm worker", threading.currentThread().name)
    event.wait()  # Wait until initialized
    print("End. I'm worker", threading.currentThread().name)


def initialize():
    print("Initializing some data")
    time.sleep(2)
    print("Unblocking the workers")
    event.set()



# Launch a bunch of worker threads
threading.Thread(target=worker).start()
threading.Thread(target=worker, name='HI_TREAD').start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker2, name="255").start()
threading.Thread(target=worker).start()

# Go initialize and eventually unlock the workers
initialize()
