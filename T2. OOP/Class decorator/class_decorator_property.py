# Property decorator

class property_(object):
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, cls):
        print('Called property from {instance} of {klass}'.format(instance=instance, klass=cls))
        return self.func(instance)

    def __set__(self, obj, value):
        print('Setting up {value} for {obj}'.format(value=value, obj=obj))
        [setattr(obj, k, v) for k, v in value.items()]


class Apple(object):

    @property_
    def get_color(self):
        print('Accessing get_color property')
        return 'red'


if __name__ == '__main__':
    apple = Apple()
    print(apple.get_color)
    apple.get_color = {'shape': 'triangle'}
    print(apple.shape)
