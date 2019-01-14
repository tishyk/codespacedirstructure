def decorator(F):
    def wrapper(*args):
        print(F)
        print('Called with args{}'.format(args))
    return wrapper

@decorator
def func(x, y):
    print(x,y)

class C(object):
    @decorator
    def method(self, x, y):
        print(x,y)
        print("This page")


if __name__ == '__main__':
    c = C()
    c.method(1,2)
    func(3,4)


"""
Here the decorator wraps either class or function.
In the first case tuple with args contains only variables passed to the function.
In the class call in args, there is also an instance of C class.
"""
