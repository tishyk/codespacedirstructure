from concurrent.futures import ProcessPoolExecutor, as_completed

import time
import multiprocessing

def func(n):
    time.sleep(n)
    print(multiprocessing.current_process().name)
    return f'I was do this task during {n} seconds'


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        p1 = executor.submit(func, 3)
        p2 = executor.submit(func, 5)
        # print(p1.result())
        # print(p2.result())
        for proc in as_completed((p1, p2)):
            print(f"Completed result: {proc.result()}")

