class Descriptor:

    def __init__(self, name):
        self.name = name


class INT(Descriptor):

    def __set__(self, instance, value):
        assert isinstance(value, int), "Value is not int"
        instance.__dict__[self.name] = value


class STR(Descriptor):

    def __set__(self, instance, value):
        assert isinstance(value, str), "Value is not str"
        instance.__dict__[self.name] = value

class A:

    def __init__(self):
        self.val_int = INT('wfwfwef')
        self.val_str = STR(123)


a = A()
a.val_int = 'qdqdqdqd'