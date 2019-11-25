
def common_elements(x, y):
    _a, _b = set(x), set(y)
    return list(_a.intersection(_b))


def a_num(string, letter):
    return string.count(letter)


def power_of_three(x):
    if x % 3 == 0:
        return True
    else:
        return False


def single_digit(x):
    _x = tuple(str(x))
    while len(_x) == 2:
        _x = str(int(_x[0]) + int(_x[1]))
    return _x


def zeros_to_the_end(x):
    for _ in range(len(x) - 1):
        for index in range(len(x) - 1):
            if x[index] == 0:
                x[index + 1], x[index] = x[index], x[index + 1]
    return x


def arithmetic_progression(x):
    delta = x[1] - x[0]
    for index in range(len(x) - 1):
        if not (x[index + 1] - x[index] == delta):
             return False
    return True


def single_num(nums):
    result = 0
    for i in nums:
        result ^= i
    return result


def find_missing(arr):
    return sorted(set(range(arr[0], arr[-1])) - set(arr))[0]


def count_elements(arr):
    i = 0
    for num in arr:
        if isinstance(num, tuple):
            break
        i = i + 1
    return i


def revert_string(string):
    s = ""
    for i in string:
        s = i + s
    return s
