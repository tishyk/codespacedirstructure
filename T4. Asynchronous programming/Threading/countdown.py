# countdown.py
# An example of defining a thread as a class

import time
import threading


class CountdownThread(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self, daemon=True)
        self.count = count

    def run(self):
        while self.count > 0:
            print("Counting down", self.count)
            self.count -= 1
            time.sleep(0)
        return self.count


# Sample execution
t1 = CountdownThread(10)
t1.start()
t2 = CountdownThread(20)
t2.start()
t2.join()
print(50000000)