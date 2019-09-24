import time
import asyncio

time.perf_counter()
start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


async def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('gr1 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr1 ended work: {}'.format(tic()))


async def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('gr2 started work: {}'.format(tic()))
    await asyncio.sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


async def gr3():
    print("Lets do some stuff while the coroutines are blocked, {}".format(tic()))
    await asyncio.sleep(1)
    print("Done!")


io_loop = asyncio.get_event_loop()
tasks = [
    io_loop.create_task(gr1()),
    io_loop.create_task(gr2()),
    io_loop.create_task(gr3())]
io_loop.run_until_complete(asyncio.wait(tasks))
io_loop.close()
print(time.perf_counter())
