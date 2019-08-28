def decorator(cls):
    class Wrapper(object):
        def __init__(self, *args):
            self.wrapped_cls = cls(*args)

        def __getattr__(self, name):
            print('Getting the {} of {}'.format(name, self.wrapped_cls))
            return getattr(self.wrapped_cls, name)

    return Wrapper


@decorator
def set_color(self):
    print("Set color")


@decorator
class C(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_color(self):
        print("Set color")


if __name__ == '__main__':
    x = C(1,2)
    print(x.x)
    x.set_color()