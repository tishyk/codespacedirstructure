# Basic example of decorator defined by class

class decorator():
    def __init__(self, func):
        print(10)
        self.func = func

    def __call__(self, *args):
        print('Called {func} with args: {args}'.format(
            func=self.func.__name__, args=args))
        print(self, args)
        return self.func(*args)


@decorator
def my_func(x, y):
    print('Function called')
    return x, y


if __name__ == '__main__':
    # Basic example of decorator defined by class
    my_func(1, 2)
