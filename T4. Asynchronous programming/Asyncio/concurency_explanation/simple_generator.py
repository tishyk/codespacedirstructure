def countdown_task(n):
    while n > 0:
        print(n)
        yield n
        n -= 1


# How many yield can be here?
# Can we use return in generator?
# Can we get data from other generator inside generator?

# def countdown_10():
#     print("Countdown function start")
#     yield from countdown_task(10)
#     print("Countdown function end")
#
#
#
# for count in countdown_10():
#     pass
