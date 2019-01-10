
def debug(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)

    return wrapper


class CWrapper:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Class wrapper for {}".format(self.func.__name__))
        return self.func(*args, **kwargs)