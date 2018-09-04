from multiprocessing import Pool
import time

def func(n):
    return n*n

if __name__ == "__main__":
    p = Pool(processes=3)
    result = p.map(func,range(1000))
    for n in result:
        print(n)