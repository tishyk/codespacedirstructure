def int_types(elements):
    for el in elements:
        if type(el) != int:
            return False

    return True


def check_arithmetic_progression(numbers):
    if type(numbers) is not list or not int_types(numbers):
        raise ValueError("Should be passed list of integers")

    if len(numbers) < 2:
        return False

    if len(numbers) == 2:
        return True

    common_difference = numbers[1] - numbers[0]
    for idx in range(2, len(numbers)):
        if numbers[idx] - numbers[idx - 1] != common_difference:
            return False

    return True