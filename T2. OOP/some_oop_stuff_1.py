# Keyword-Only Args

def recv(maxsize, *args, block=True):
    print(maxsize, args, block)

recv(100, 11, 12, 13, 14, 16, 17)


class SomeClass:
    class_var = 10  # class variable

    def __init__(self, inst_var):
        self.inst_var = inst_var  # instance variable

    def inst_method(self):
        print('Inst method')  # instance method


print(SomeClass.class_var)
bc = SomeClass(20)
print(bc.inst_var)
print(bc.inst_method())


class AnotherClass:  # ac = AnotherClass()
    def imethod(self):  # ac.imethod()
        pass

    @classmethod
    def cmethod(cls):  # AnotherClass.cmethod()
        pass

    @staticmethod
    def smethod():  # AnotherClass.smethod()
        pass


class BaseClass:
    # super and mro explanation
    def basemethod(self, var):
        print("This is a {} method".format(self.__class__.__name__))
        return var + 10


class SClass(BaseClass):
    def basemethod(self, var):  # method overloading
        print("Overloaded method")
        base_var = super().basemethod(var)
        print(base_var)


sc = SClass()
sc.basemethod(100)
# print(sc.__mro__) # __mro__ is a class variable
print(SClass.__mro__) # add AnotherClass to SClass bases
