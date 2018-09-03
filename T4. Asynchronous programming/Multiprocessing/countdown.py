# countdownp.py
#
# Example of launching a process with the multiprocessing module

import time
import multiprocessing


class CountdownProcess(multiprocessing.Process):
    def __init__(self, count):
        multiprocessing.Process.__init__(self)
        self.count = count

    def run(self):
        while self.count > 0:
            print("Counting down", self.count)
            self.count -= 1
            time.sleep(2)
        return


if __name__ == '__main__':
    p1 = CountdownProcess(10)  # Create the process object
    p1.start()  # Launch the process

    p2 = CountdownProcess(20)  # Create another process
    p2.start()  # Launch
