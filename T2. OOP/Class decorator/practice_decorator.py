# create function/class wrapper for the next methods
# decorator print the name of decorated function inside decorator
# object.__name__


@debug
def add(x, y):
    return x + y

@debug
def sub(x, y, z):
    return x - y, z

@CWrapper
def mul(x, y, z):
    return x * y, z

@CWrapper
def div(x, y):
    return x / y

