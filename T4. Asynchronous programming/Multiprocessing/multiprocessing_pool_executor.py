from concurrent.futures import ProcessPoolExecutor, as_completed

import time
import multiprocessing

def func(n):
    time.sleep(n)
    print(multiprocessing.current_process().name)
    return f'I was do this task during {n} seconds'


if __name__ == "__main__":
    with ProcessPoolExecutor(2) as executor:
        p1 = executor.submit(func, 4)
        p2 = executor.submit(func, 1)
        print(p1.result(), 1)
        print(p2.result(), 2)
        for proc in as_completed((p1, p2)):
            print(f"Completed result: {proc.result()}")

