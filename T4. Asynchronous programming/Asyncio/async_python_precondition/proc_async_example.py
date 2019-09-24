import requests
import time
from multiprocessing import Process

urls = ['http://www.google.com', 'http://devdocs.io', 'http://www.python.org']


def call_url(url):
    print('Starting {}'.format(url))
    response = requests.get(url)
    data = response.text
    print('{}: {} bytes: {}'.format(url, len(data), data[:30]))
    return data


time.perf_counter()

if __name__ == '__main__':
    threads = [Process(target=call_url, args=(url,)) for url in urls]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    print('Done', time.perf_counter())
