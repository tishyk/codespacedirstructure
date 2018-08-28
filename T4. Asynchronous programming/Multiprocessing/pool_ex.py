# poolmp.py
#
# An example of using multiprocessing pools

# A function that does a reasonable amount of processing
import hashlib


def compute_digest(filename):
    digest = hashlib.sha512()
    f = open(filename, 'rb')
    while True:
        chunk = f.read(8192)
        if not chunk: break
        digest.update(chunk)
    f.close()
    return digest.digest()


import os
import time

TOPDIR = "C\\Users\\Public"  # Change for your machine


# A sequential function that walks a directory and computes
# SHA-512 hashes for all files

def sequential():
    start = time.time()
    digest_map = {}
    for path, dirs, files in os.walk(TOPDIR):
        for name in files:
            fullname = os.path.join(path, name)
            if os.path.exists(fullname):
                digest_map[fullname] = compute_digest(fullname)
    end = time.time()
    print(end - start, "seconds")
    return digest_map


import multiprocessing


# A function that does the same calculation using pools
def parallel():
    start = time.time()
    p = multiprocessing.Pool(2)  # Make a process pool
    digest_map = {}
    for path, dirs, files in os.walk(TOPDIR):
        for name in files:
            fullname = os.path.join(path, name)
            if os.path.exists(fullname):
                digest_map[fullname] = p.apply_async(compute_digest, (fullname,))

    # Go through the final dictionary and collect results
    for filename, result in digest_map.items():
        digest_map[filename] = result.get()
    end = time.time()
    print(end - start, "seconds")
    return digest_map


# Note : due to the disk buffer cache, you'll probably want to run
# this program twice and look at the results of the second run
# to get a better picture of performance (the sequential execution
# will be penalized on the first run if there is a cold disk cache)

map1 = sequential()
map2 = parallel()
assert map1 == map2
