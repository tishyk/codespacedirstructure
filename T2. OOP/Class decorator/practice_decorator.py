# create function/class wrapper for the next methods
# decorator print the name of decorated function
# object.__name__

@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@CWrapper
def mul(x, y):
    return x * y

@CWrapper
def div(x, y):
    return x / y

