import asyncio
from math import sqrt
from main_async import fibonacci

async def search(iterable, predicate):
   for item in iterable:
      if await predicate(item):
         return item
      await asyncio.sleep(0)
   raise ValueError('Not found')

async def is_prime(x):
   if x < 2:
      return False
   for i in range(2, int(sqrt(x)+1)):
      if x % i == 0:
         return False
      await asyncio.sleep(0)
   return True

async def monitored_search(iterable, predicate, future):
   try:
      found_item = await search(iterable, predicate)
   except ValueError as not_found:
      future.set_exception(not_found)
   else: # no exception
      future.set_result(found_item)

async def twenty_digit_prime(x):
   return (await is_prime(x))and len(str(x)) == 12

async def monitor_feature(future, interval):
   while not future.done():
      print("Waiting ..")
      await asyncio.sleep(interval)
   print("Done!")

"""
# Future
loop = asyncio.get_event_loop()
future = loop.create_future()
coro_obj = monitored_search(fibonacci(), twenty_digit_prime, future)
loop.create_task(coro_obj)
loop.create_task(monitor_feature(future, 1))
loop.run_until_complete(future)
print(future.result())
loop.close()
"""


# Task
loop = asyncio.get_event_loop()
future = loop.create_future()
coro_obj = search(fibonacci(), twenty_digit_prime)
search_task = loop.create_task(coro_obj)

loop.create_task(monitor_feature(search_task, 1))
loop.run_until_complete(search_task)
print(search_task.result())


