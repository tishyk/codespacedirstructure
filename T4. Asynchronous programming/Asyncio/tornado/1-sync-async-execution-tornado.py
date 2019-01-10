from tornado import gen
import time
from tornado import ioloop
import requests

response = None


@gen.coroutine
def foo():
    global response
    print('Running in foo')
    while not response:
        yield time.sleep(1)
        print('waiting..', response)
    else:
        print('Explicit context switch to foo again', response)

@gen.coroutine
def bar():
    global response
    print('Explicit context to bar')
    response = yield requests.get('https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e?_utm_source=1-2-2')
    print('Implicit context switch back to bar')
    return response

@gen.coroutine
def main():
    yield [foo(), bar()]


ioloop = ioloop.IOLoop.current()
ioloop.run_sync(main)

