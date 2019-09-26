"""
Basically what is happening here is an async method,
when executed, returns a coroutine which can then be awaited.
"""

import asyncio
import aiohttp
import time

urls = ['http://www.google.com',
        'http://devdocs.io',
        'http://www.python.org']


async def call_url(url):
    print('Starting {}'.format(url))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            print('{}: {} bytes: {}'.format(url, len(data), data[:30]))
    return data


time.perf_counter()
futures = [call_url(url) for url in urls]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
print('Done', time.perf_counter())
