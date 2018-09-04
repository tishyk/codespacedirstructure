# countdown.py
#
# Example of launching a process with the multiprocessing module

import time
import multiprocessing
import threading


class CountdownProcess(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self)
        self.count = count

    def run(self):
        while self.count > 0:
            print("Counting down", self.count)
            self.count -= 1
        return


if __name__ == '__main__':
    # p1 = CountdownProcess(10)  # Create the process object
    # p1.start()  # Launch the process
    #
    # p2 = CountdownProcess(20)  # Create another process
    # p2.start()  # Launch

    [CountdownProcess(i).start() for i in range(100000)]