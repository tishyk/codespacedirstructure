import requests
import time
urls = ['http://www.google.com', 'http://devdocs.io', 'http://www.python.org']


def call_url(url):
    print('Starting {}'.format(url))
    response = requests.get(url)
    data = response.text
    print('{}: {} bytes: {}'.format(url, len(data), data[:30]))
    return data

time.clock()
[call_url(url) for url in urls]
print('Done', time.clock())