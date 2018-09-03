import time

DELAY = 0.1

def preheat_oven(target_temp):
    temp = 100
    while temp < target_temp:
        time.sleep(DELAY)
        temp += 100
        print("preheat:: temp is now {}".format(temp))

def mix_ingredients(num):
    for i in range(num):
        time.sleep(DELAY)
        print("mix_ingredients:: mixing things {}".format(i))


def bake_cake(minutes):
    for i in range(0, minutes, 4):
        time.sleep(DELAY)
        print("bake_cake:: baking for {} minutes".format(i))

def make_frosting(minutes):
    for i in range(0, minutes, 4):
        time.sleep(DELAY)
        print("make_frosting:: making frosting for {} minutes".format(i))

def apply_frosting(minutes=4):
    for i in range(0, minutes, 2):
        time.sleep(DELAY)
        print("apply_frosting:: frosting for {} minutes".format(i))

if __name__ == "__main__":
    preheat_oven(400)
    mix_ingredients(3)
    bake_cake(16)
    make_frosting(12)
    apply_frosting()