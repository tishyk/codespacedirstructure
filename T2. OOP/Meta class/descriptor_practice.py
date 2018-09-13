
class MyDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        # instance: is the instance being manipulated
        # e.q. CPlatform instance
        print("Get name:", self.name)
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print("Set value:", value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print("Delete:", self.name)
        del instance.__dict__[self.name]

class INT(MyDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected type 'int'")
        super().__set__(instance, value)

class DarwinPlatform:
    platform = INT('platform')
    def __init__(self, platform):
        self.platform = platform

dwpl = DarwinPlatform(10)
dwpl.platform
dwpl.platform = "new platform"
del dwpl.platform