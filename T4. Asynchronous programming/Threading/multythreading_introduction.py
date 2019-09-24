import time
import threading

def calc_square(numbers):
    print("calculate square numbers")
    for n in numbers:
        time.sleep(1)
        print('square:', n * n)

def calc_cube(numbers):
    print("calculate cube of numbers")
    for n in numbers:
        time.sleep(1)
        print('cube:', n * n * n)

arg = [2, 3, 8, 9]

t = time.time()

t1 = threading.Thread(target=calc_square, args=(arg,), daemon=True)
t2 = threading.Thread(target=calc_cube, args=(arg,))

t1.start()
t1.join()
t2.start()
t2.join()

print("done in : ", time.time() - t)
print("I am done with all my work now!")
