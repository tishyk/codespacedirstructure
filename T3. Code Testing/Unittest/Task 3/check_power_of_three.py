import math


def check_power_of_three(number):
    if type(number) != int:
        raise ValueError("Number should be type int")

    return math.log(number, 3).is_integer()