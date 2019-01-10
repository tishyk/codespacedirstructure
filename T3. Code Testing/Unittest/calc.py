# This is a base code for testing with pytest and unittest or nose
# we will start from unitest because of it's builtin library
# unitest cmd for testing - testing>python -m unittest test_math.py
# pytest cmd for testing - python -m pytest   or py.test -v


def add(x,y):
    """Add function"""
    return x + y

def subtract(x,y):
    """Subtarct function"""
    return x - y

def multiply(x,y):
    """Multiply Function"""
    return x * y

def divide(x,y):
    assert y != 0, "Can not devide by zero!"
    return x / y


# Simple code testing - print function
# print(divide(10, 0))
# But Assertion Error is possible
