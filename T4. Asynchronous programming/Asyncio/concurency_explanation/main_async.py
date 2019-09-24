import asyncio
import time
from math import sqrt


from main import *

def fibonacci():
   yield 2
   a = 2
   b = 1
   while True:
      yield b
      a, b = b, a + b

async def is_prime(x):
   if x < 2:
      return False
   for i in range(2, int(sqrt(x)+1)):
      if x % i == 0:
         return False
      await asyncio.sleep(0)
   return True

async def search(iterable, predicate):
   for item in iterable:
      if predicate(item):
         return item
      await asyncio.sleep(0)
   raise ValueError('Not found')

async def print_matches(iterable, predicate):  
   for item in iterable:
      matches = await predicate(item)
      if matches:
         print("Found: ", item)

async def repetitive_msg(msg, interval):
   while True:
      print(msg)
      await asyncio.sleep(interval)

scheduler = asyncio.get_event_loop()
#scheduler.create_task(repetitive_msg("Interval message", 2))
#scheduler.create_task(print_matches(fibonacci(), is_prime))
#scheduler.run_forever()
