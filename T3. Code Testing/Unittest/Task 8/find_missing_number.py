def int_type(numbers):
    for number in numbers:
        if type(number) is not int:
            return False

    return True


def find_missing_number(numbers):
    if type(numbers) is not list or not int_type(numbers) or len(numbers) < 2:
        raise ValueError("Should be passed list of integers (at least 2)")

    prev_value = numbers[0]
    for i in numbers[1:]:
        if i != prev_value + 1:
            return prev_value + 1

        prev_value = i

    return "Not found missing number"