def deco(func):
    print('before wrapper')
    def wrapper(*args):
        print('Wrapper for function {}'.format(func.__name__))
        return func(*args)
    print('after wrapper')
    return wrapper

@deco
def decorated(*args):
    print("Inside function")
    print(*args)

decorated(1,2,3, "Hi decorator")