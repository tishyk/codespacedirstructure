import asyncio

DELAY = 0.1


@asyncio.coroutine
def preheat_oven(target_temp):
    temp = 100
    while temp < target_temp:
        yield from asyncio.sleep(DELAY)
        temp += 100
        print("preheat:: temp is now {}".format(temp))
    return True


@asyncio.coroutine
def mix_ingredients(*ingredients):
    result = 0
    for i in ingredients:
        result += i
        yield from asyncio.sleep(DELAY)
        print("mix_ingredients:: mixing things {}".format(i))
    return result


@asyncio.coroutine
def bake_cake(batter, minutes):
    for i in range(0, minutes, 4):
        yield from asyncio.sleep(DELAY)
        print("bake_cake:: baking for {} minutes".format(i))
    return True


@asyncio.coroutine
def make_frosting(minutes):
    for i in range(0, minutes, 4):
        yield from asyncio.sleep(DELAY)
        print("make_frosting:: making frosting for {} minutes".format(i))
    return True


@asyncio.coroutine
def apply_frosting(cake, frosting, minutes=4):
    for i in range(0, minutes, 2):
        yield from asyncio.sleep(DELAY)
        print("apply_frosting:: frosting for {} minutes".format(i))
    return True


@asyncio.coroutine
def doit():
    is_preheated, batter = yield from asyncio.gather(
        preheat_oven(400),
        mix_ingredients(1, 2, 3))

    cake, frosting = yield from asyncio.gather(
        bake_cake(batter, 16),
        make_frosting(12))

    final = yield from apply_frosting(cake, frosting)
    print("Final product: {}".format(final))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(doit())
