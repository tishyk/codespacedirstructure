# countdown2.py
# An example of launching a function into a separate thread

import time
import threading


def countdown(count):
    while count > 0:
        print("Counting down", count)
        count -= 1
        time.sleep(2)
    return


# Sample execution
t1 = threading.Thread(target=countdown, args=(10,))
t1.start()
t2 = threading.Thread(target=countdown, args=(20,))
t2.start()
