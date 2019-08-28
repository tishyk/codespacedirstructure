def debugattr(cls):
    origin_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print("Get attribute:", name)
        return origin_getattribute(self, name)

    cls.__getattribute__ = __getattribute__
    return cls


class DebugMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        cls_obj = super().__new__(cls, clsname, bases, clsdict)
        cls_obj = debugattr(cls_obj)
        return cls_obj


class Platform(metaclass=DebugMeta):
    def __init__(self, *args, **kwargs):
        [self.__setattr__('var{}'.format(i), var) for i, var in enumerate(args)]
        self.__dict__.update(kwargs)


platform = Platform(1, 2, 5, 8, 90, hi=True, msg="Greatings")
print(platform.msg)
pass

# All values in Python have  a type

x = 10
type(x)
s = "Hello"
type(s)


# etc

# Classes define new types

class Dot:
    def __init__(self, dot):
        self.dot = dot


dot = Dot(0)
type(dot)
# The class is the type of instance created
# The class is a callable that creates instances

# Check type of int, str etc built in classes
type(Dot)
print(isinstance(Dot, type))  # this mean classes are instances types but created objects has base object - object


# class type:
#     pass


print(type)  # this class creates new "type" objects


# It's used while class defining


# Consider a class DashDot

class DashDot(Dot):
    def __init__(self, dash):
        self.dash = dash


dashdot = DashDot((1, 1))
# What are it's components?
# Name - "DashDot"
# Base classes - (Dot)
# Function __init__

# Whats happens during class definition?

# Step 1. Body of class is isolated

body = """def __init__(self, dash):
        self.dash= dash
        """

# Step 2. The class dictionary is created

clsdict = type.__prepare__("DashDot", (Dot,))
print(clsdict)

# This dictionary serves as local namespace for statements in the class body
# It's a simple dictionary by default

# Step 3: Body is executed in returned dict (clsdict)

exec(body, globals(), clsdict)  # clsdit population here
print(clsdict)

# Step 4. Class is constructed from it's name, base classes, and the dictionary

DashDot = type("DashDot", (Dot,), clsdict)
dashdot2 = DashDot((0, 0))
print(dashdot2)


# How to change a metaclass from default type to any other?
# Keyword argument is - metaclass
# Sets the class used for creating type

class BaseClass(metaclass=type):   # it's set to type by default. You can change it to something else
    class_var = 10  # class variable

    def __init__(self, inst_var):
        self.inst_var = inst_var  # instance variable

    def inst_method(self):
        print('Inst method')  # instance method

print(BaseClass(1000))

# We are typically inherit from type and redefine __new__ or __init__

class mytype(type):
    def __new__(cls, cls_name, bases, clsdict):
        print("Class creation")
        if len(bases) > 1:
            raise TypeError("Too much base classes")
        clsobj = super().__new__(cls, cls_name, bases, clsdict)
        return clsobj

    def meta_method(cls):
        print("Before cls object creation",
              cls.__dict__)

class BaseClass(metaclass=mytype):   # it's set to type by default. You can change it to something else
    class_var = 10  # class variable

    def __init__(self, inst_var):
        self.inst_var = inst_var  # instance variable

    def inst_method(self):
        print('Inst method')  # instance method

# print(BaseClass(1000))

class A(BaseClass): pass
class B(BaseClass): pass
A.meta_method()

a = A('Hello')
#a.meta_method()  #Failed with AttributeError: 'A' object has no attribute 'meta_method'
#class C(A,B): pass  # should failed

# Metaclass get infomation about class definiton at the time of definition
# -- Can inspect this data
# -- Can modify this data
# Essentially, similar to a class decorator
# Metaclasses propogate down hierarchies
