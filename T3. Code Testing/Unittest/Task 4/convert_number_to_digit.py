def digit(number):
    return number < 10


def decomposite_number_to_digits(number):
    return [int(i) for i in str(number)]


def convert_number_to_digit(number):
    if type(number) != int or number < 0:
        raise ValueError("Input value should be positive integer")

    if digit(number):
        return number

    return convert_number_to_digit(sum(decomposite_number_to_digits(number)))