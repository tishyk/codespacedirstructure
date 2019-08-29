import sys

class DarwinPlatform:
    platform = "Mac"
    # do something for specific platform

class LinuxPlatform:
    platform = "Linux"

class WindowsPlatform:
    platform = "Windows"

class CPlatform:
    # Base object for platform dependent test
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if 'darwin' in sys.platform:
            platform = DarwinPlatform
        elif 'linux' in sys.platform:
            platform = LinuxPlatform
        else:
            platform = WindowsPlatform
        instance.__dict__.update(platform.__dict__)
        return instance

    def __init__(self, *args, **kwargs):
        print("Init method", args, kwargs)


bp = CPlatform(test_path="path to test", cycle=2)
print(bp.platform)

#
# class CTest(CPlatform):
#     def __init__(self, name, *args, **kwargs):
#         self.name = name
#         self.steps = kwargs.get('steps', [])
#
#     def __del__(self):
#         # do something on script exit or manual object deletion
#         self.steps = []
#         del self  # not recommended
#
#     def __str__(self):
#         return ("{}: {}".format(self.__class__.__name__, self.name))
#
#     def __repr__(self):
#         """
#         Representing your Classes
#         It’s often useful to have a string representation of a class. In Python, there’s a few methods
#         that you can implement in your class definition to customize how built in functions that return
#         representations of your class behave.
#         __str__(self) Defines behavior for when str() is called on an instance of your class.
#         __repr__(self) Defines behavior for when repr() is called on an instance of your class. The
#         major difference between str() and repr() is intended audience. repr() is intended to
#         produce output that is mostly machine-readable (in many cases, it could be valid Python
#         code even), whereas str() is intended to be human-readable.
#         __unicode__(self) Defines behavior for when unicode() is called on an instance of your class.
#         unicode() is like str(), but it returns a unicode string. Be wary: if a client calls str()
#         on an instance of your class and you’ve only defined __unicode__(), it won’t work. You
#         should always try to define __str__() as well in case someone doesn’t have the luxury of
#         using unicode.
#         __format__(self, formatstr) Defines behavior for when an instance of your class is used in
#         new-style string formatting. For instance, "Hello, 0:abc!".format(a) would lead to
#         the call a.__format__("abc"). This can be useful for defining your own numerical or
#         string types that you might like to give special formatting options.
#         __hash__(self) Defines behavior for when hash() is called on an instance of your class. It
#         has to return an integer, and its result is used for quick key comparison in dictionaries.
#         Note that this usually entails implementing __eq__ as well. Live by the following rule: a
#         == b implies hash(a) == hash(b).
#         __nonzero__(self)2x Defines behavior for when bool() is called on an instance of your class.
#         Should return True or False, depending on whether you would want to consider the instance
#         to be True or False.
#         __bool__(self)3x Defines behavior for when bool() is called on an instance of your class.
#         Should return True or False, depending on whether you would want to consider the instance
#         to be True or False.
#         __dir__(self) : Defines behavior for when dir() is called on an instance of your class. This
#         method should return a list of attributes for the user. Typically, implementing __dir_-
#         _ is unnecessary, but it can be vitally important for interactive use of your classes if you
#         redefine __getattr__ or __getattribute__ (which you will see in the next section) or
#         are otherwise dynamically generating attributes.
#         """
#         return ("<-- {}: {} -->".format(self.__class__.__name__, self.name))
#
#     def __cmp__(self, test_obj):  # The __cmp__() special method is no longer honored in Python 3.
#         assert isinstance(test_obj, CTest), "Not a test object compared"
#         return test_obj.name == self.name
#
#     def __eq__(self, test_obj):
#         assert isinstance(test_obj, CTest), "Not a test object compared"
#         return test_obj.name == self.name
#         """Operator	Method
#             ==	__eq__
#             !=	__ne__
#             <	__lt__
#             <=	__le__
#             >	__gt__
#             >=	__ge__"""
#         # Create step_lst with test step count and compare tests
#
#     def __neg__(self):
#         """
#         Unary operators and functions only have one operand, e.g. negation, absolute value, etc.
#         __pos__(self) Implements behavior for unary positive (e.g. +some_object)
#         __neg__(self) Implements behavior for negation (e.g. -some_object)
#         __abs__(self) Implements behavior for the built in abs() function.
#         __invert__(self) Implements behavior for inversion using the ~ operator.
#         __round__(self, n) Implements behavior for the buil in round() function. n is the number
#         of decimal places to round to.
#         __floor__(self) : Implements behavior for math.floor(), i.e., rounding down to the nearest
#         integer.
#         __ceil__(self) : Implements behavior for math.ceil(), i.e., rounding up to the nearest
#         integer.
#         __trunc__(self) : Implements behavior for math.trunc(), i.e., truncating to an integral
#         """
#         self.steps = self.steps[::-1]
#
#     def __add__(self, test_obj):
#         """
#         Normal arithmetic operators
#         Now, we cover the typical binary operators (and a function or two): +, -, * and the like. These
#         are, for the most part, pretty self-explanatory.
#         __add__(self, other) Implements addition.
#         __sub__(self, other) Implements subtraction.
#         __mul__(self, other) Implements multiplication.
#         __floordiv__(self, other) Implements integer division using the // operator.
#         __div__(self, other) Implements division using the / operator.
#         __truediv__(self, other) Implements true division. Note that this only works when from
#         __future__ import division is in effect.
#         __mod__(self, other) Implements modulo using the % operator.
#         __divmod__(self, other) Implements behavior for long division using the divmod() built in function.
#         __pow__ Implements behavior for exponents using the ** operator.
#         """
#         assert isinstance(test_obj,
#                           CTest), "Not a test object added"  # add int check for one more step addition possibility
#         name = "{}_{}".format(self.name, test_obj.name)
#         return CTest(name, steps=self.steps + test_obj.steps)
#
#     def __radd__(self, test_obj):
#         """
#         The reflected equivalent is the same thing, except with the
#         operands switched around:
#         other + some_object
#         So, all of these magic methods do the same thing as their normal equivalents, except the
#         perform the operation with other as the first operand and self as the second, rather than the
#         other way around. In most cases, the result of a reflected operation is the same as its normal
#         equivalent, so you may just end up defining __radd__ as calling __add__ and so on. Note
#         that the object on the left hand side of the operator (other in the example) must not define
#         (or return NotImplemented) for its definition of the non-reflected version of an operation. For
#         instance, in the example, some_object.__radd__ will only be called if ‘other‘ does not define
#         __add__.
#         __radd__(self, other) Implements reflected addition.
#         __rsub__(self, other) Implements reflected subtraction.
#         __rmul__(self, other) Implements reflected multiplication.
#         __rfloordiv__(self, other) Implements reflected integer division using the // operator.
#         __rdiv__(self, other) Implements reflected division using the / operator.
#         __rtruediv__(self, other) Implements reflected true division. Note that this only works
#         when from __future__ import division is in effect.
#         __rmod__(self, other) Implements reflected modulo using the % operator.
#         __rdivmod__(self, other) Implements behavior for long division using the divmod() built
#         in function, when divmod(other, self) is called.
#         __rpow__ Implements behavior for reflected exponents using the ** operator.
#         __rlshift__(self, other) Implements reflected left bitwise shift using the << operator.
#         __rrshift__(self, other) Implements reflected right bitwise shift using the >> operator.
#         __rand__(self, other) Implements reflected bitwise and using the & operator.
#         __ror__(self, other) Implements reflected bitwise or using the | operator.
#         __rxor__(self, other) Implements reflected bitwise xor using the ^ operator.
#
#         """
#
#         assert isinstance(test_obj, CTest), "Not a test object added. Reflected addition"
#         return self.__add__(test_obj, self)
#
#     def __iadd__(self, test_obj):
#         """
#         Python also has a wide variety of magic methods to allow custom behavior to be defined
#         for augmented assignment. You’re probably already familiar with augmented assignment, it
#         combines “normal” operators with assignment. If you still don’t know what I’m talking about,
#         here’s an example:
#         x = 5
#         x += 1 # in other words x = x + 1
#         Each of these methods should return the value that the variable on the left hand side should
#         be assigned to (for instance, for a += b, __iadd__ might return a + b, which would be assigned
#         to a). Here’s the list:
#         __iadd__(self, other) Implements addition with assignment.
#         __isub__(self, other) Implements subtraction with assignment.
#         __imul__(self, other) Implements multiplication with assignment.
#         __ifloordiv__(self, other) Implements integer division with assignment using the //= operator.
#         __idiv__(self, other) Implements division with assignment using the /= operator.
#         __itruediv__(self, other) Implements true division with assignment. Note that this only
#         works when from __future__ import division is in effect.
#         __imod__(self, other) Implements modulo with assignment using the %= operator.
#         __ipow__ Implements behavior for exponents with assignment using the **= operator.
#         __ilshift__(self, other) Implements left bitwise shift with assignment using the <<= operator.
#         __irshift__(self, other) Implements right bitwise shift with assignment using the >>= operator.
#         __iand__(self, other) Implements bitwise and with assignment using the &= operator.
#         __ior__(self, other) Implements bitwise or with assignment using the |= operator.
#         __ixor__(self, other) Implements bitwise xor with assignment using the ^= operator.
#         """
#         print("Add steps:{} to {} test".format(test_obj.steps, self.name))
#         assert isinstance(test_obj, CTest), "Not a test object. Addition with assignment"
#         self.steps.extend(test_obj.steps)
#         return self
#
#     def __int__(self):
#         """
#         Type conversion magic methods
#         Python also has an array of magic methods designed to implement behavior for built in type
#         conversion functions like float(). Here they are:
#         __int__(self) Implements type conversion to int.
#         __long__(self) Implements type conversion to long.
#         __float__(self) Implements type conversion to float.
#         __complex__(self) Implements type conversion to complex.
#         __oct__(self) Implements type conversion to octal.
#         __hex__(self) Implements type conversion to hexadecimal.
#         __index__(self) Implements type conversion to an int when the object is used in a slice
#         expression. If you define a custom numeric type that might be used in slicing, you should
#         define __index__.
#         __trunc__(self) Called when math.trunc(self) is called. __trunc__ should return the
#         value of self truncated to an integral type (usually a long).
#         __coerce__(self, other) Method to implement mixed mode arithmetic. __coerce__ should
#         return None if type conversion is impossible. Otherwise, it should return a pair (2-tuple)
#         of self and other, manipulated to have the same type.
#         """
#         # do something on int(test_object) action
#         print("Delete substeps call if were present")
#         return len(self.steps)
#     #
#     # def __getattr__(self, item):  # for not implemented attributes only
#     #     print('Get attr {}'.format(item))
#     #     return 'not implemented'
#     #
#     # def __setattr__(self, item, value):  # for not implemented attributes only
#     #     self.__dict__[item] = value
#     #     return 'not implemented
#     #
#     # def __getattribute__(self, item):
#     #     print("Get attribute: {}".format(item))
#     #     return super().__getattribute__(item)
#
#     def __enter__(self):
#         print("Get __enter__ method")
#         # need to have at least one class/instance avriable for enter and exit methods
#         self.filename = self.name
#         return self.fileobj
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Exit log")
#         self.fileobj.close()
#
# class BasicDescriptor:
#     def __init__(self, name=None):
#         self.name = name  # name of attribute being stored. A key in the instance dict
#
#     def __get__(self, instance, cls):
#         print("Get instance {} name: {}".format(instance, self.name))
#         if instance is None:
#             return self
#         else:
#             # Direct manipulation of the instance dictionary
#             return instance.__dict__[self.name]
#
#     def __set__(self, instance, value):
#         # Direct manipulation of the instance dictionary
#         instance.__dict__[self.name] = value
#
#     def __delete__(self, instance):
#         # Direct manipulation of the instance dictionary
#         del instance.__dict__[self.name]
#
# class MyDescriptor:
#     def __init__(self, name):
#         self.name = name
#
#     def __get__(self, instance, cls):
#         # instance: is the instance being manipulated
#         # e.q. CPlatform instance
#         print("Get name:", self.name)
#         return instance.__dict__[self.name]
#
#     def __set__(self, instance, value):
#         print("Set value:", value)
#         instance.__dict__[self.name] = value
#
#     def __delete__(self, instance):
#         print("Delete:", self.name)
#         del instance.__dict__[self.name]
#
# class INT(MyDescriptor):
#     def __set__(self, instance, value):
#         if not isinstance(value, int):
#             raise TypeError("Expected type 'int'")
#         super().__set__(instance, value)
#
# class DarwinPlatform:
#     name = MyDescriptor('name')
#     def __init__(self, platform):
#         self.platform = platform
#
# dwpl = DarwinPlatform(10)
# dwpl.name
# dwpl.platform = "new platform"
# del dwpl.platform
