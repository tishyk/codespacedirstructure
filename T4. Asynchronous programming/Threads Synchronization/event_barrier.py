# event_barrier.py
#
# An example of using an event to set up a barrier synchronization

import threading
import time

init = threading.Event()


def worker():
    init.wait()  # Wait until initialized
    print("I'm worker", threading.currentThread().name)


def initialize():
    print("Initializing some data")
    time.sleep(10)
    print("Unblocking the workers")
    init.set()


# Launch a bunch of worker threads
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()
threading.Thread(target=worker).start()

# Go initialize and eventually unlock the workers
initialize()
