def countdown_task(n):
    yield
    while n > 0:
        yield n
        n -= 1
        # return 10


for value in countdown_task(10):
    print(value)


# Can we yield nothing? What for?
# How many yield can be here?
# Can we use return in generator?
# Can we get data from other generator inside generator?


def countdown_task_10():
    print("Countdown function start")
    for i in countdown_task(10):
        yield i
    print("Countdown function end")


def countdown_10():
    print("Countdown function start")
    yield from countdown_task(10)
    print("Countdown function end")


for count in countdown_10():
    print(count)
