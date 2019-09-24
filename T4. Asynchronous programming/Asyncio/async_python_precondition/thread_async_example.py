import requests
import time
from threading import Thread

urls = ['http://www.google.com', 'http://devdocs.io', 'http://www.python.org']


def call_url(url):
    print('Starting {}'.format(url))
    response = requests.get(url)
    data = response.text
    print('{}: {} bytes: {}'.format(url, len(data), data[:30]))
    return data


time.perf_counter()
threads = [Thread(target=call_url, args=(url,)) for url in urls]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
print('Done', time.perf_counter())
