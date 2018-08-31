"""
We are not looking for errors, because errors get passed up the stack correctly.
We can return an object if we want.
We can start all coroutines, and gather them later.
No callbacks
Line 'data = yield from response.text()' doesn’t execute until line 9 is completely done.
"""

import asyncio
import aiohttp

urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']

@asyncio.coroutine
"""
Coroutines are special functions that work similarly to Python generators,
on await they release the flow of control back to the event loop.
A coroutine needs to be scheduled to run on the event loop,
once scheduled coroutines are wrapped in Tasks which is a type of Future.
"""
def call_url(url):
    print('Starting {}'.format(url))
    response = yield from aiohttp.get(url) #aiohttp.get method was deprecated
    data = yield from response.text()
	"""
	Coroutines contain yield points where we define possible points 
	where a context switch can happen if other tasks are pending,
	but will not if no other task is pending.
	"""
    print('{}: {} bytes: {}'.format(url, len(data), data))
    return data

""" New syntax from python 3.7 

async def call_url(url):
    print('Starting {}'.format(url))
    response = await aiohttp.get(url)
    data = await response.text()
	
	Coroutines contain yield points where we define possible points 
	where a context switch can happen if other tasks are pending,
	but will not if no other task is pending.
    print('{}: {} bytes: {}'.format(url, len(data), data))
    return data	
"""
"""
Futures	are objects that represent the result of a task that may or may not have been executed.
This result may be an exception.
"""
futures = [call_url(url) for url in urls]   


"""
An event loop essentially manages and distributes the execution of different tasks. 
It registers them and handles distributing the flow of control between them
"""
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))