def fib(count):
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b


def fibonacci_sequence_generate(count):
    if type(count) != int or count < 0:
        raise ValueError("Should be passed value typed int")

    return list(fib(count))
