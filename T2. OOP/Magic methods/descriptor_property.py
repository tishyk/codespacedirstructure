
class Property:
    def __init__(self, attribute):
        self.attribute = attribute

    def __get__(self, instance, cls):
        # instance: is the instance being manipulated
        # e.q. CPlatform instance
        print("Get attribute and call it:", self.attribute)
        attribute = instance.__dict__[self.attribute]
        assert callable(attribute), "Object is not callable"
        return attribute()

    def __set__(self, instance, new_value):
        print("Set attribute:", new_value)
        assert callable(new_value), "Object is not callable"
        instance.__dict__[self.attribute] = new_value

    def __delete__(self, instance):
        print("Delete attribute:", self.attribute)
        del instance.__dict__[self.attribute]

class MyPropertyUsage:
    my_property = Property('some_function')

    def __init__(self):
        self.my_property = self.some_function

    def some_function(self):
        print("Hi, I'm function of property object")
        return True

myprop = MyPropertyUsage()
myprop.my_property
myprop.my_property = help
myprop.my_property
del myprop.my_property
