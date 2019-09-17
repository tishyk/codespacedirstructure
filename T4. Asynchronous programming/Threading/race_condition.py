# race.py
# A simple example of a race condition

import threading

x = 0  # A shared value

COUNT = 10000000

def foo():
    global x
    for i in range(COUNT):
        x += 1

def bar():
    global x
    for i in range(COUNT):
        x -= 1

t1 = threading.Thread(target=foo)
t2 = threading.Thread(target=bar)

t1.start()
t2.start()



print(x)
