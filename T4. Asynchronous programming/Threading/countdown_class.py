# countdown.py
# An example of defining a thread as a class

import time
import threading

class CountdownThread(threading.Thread):
    def __init__(self, count, t_to_sync=None):
        threading.Thread.__init__(self)
        self.count = count
        self.t = t_to_sync

    def run(self):
        while self.count > 0:
            if self.t and not self.t.is_alive():
                print(self.t.is_alive(),
                      self.t.name)
                break
            print("Counting down", self.count)
            self.count -= 1
            #time.sleep(0.1)
        return self.count


# Sample execution
t1 = CountdownThread(10)
t2 = CountdownThread(20, t1)

t1.start()
t2.start()
t1.name


print(50000000)