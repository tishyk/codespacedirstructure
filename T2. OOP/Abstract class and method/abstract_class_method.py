
class AbstractClass: # This is not an abstract class
    def do_something(self):
        pass

class B(AbstractClass):  # we can instantiate an instance from
    pass                 # we are not required to implement do_something in the class defintition of B

a = AbstractClass()
b = B()

from abc import ABC, abstractmethod


class AbstractClassExample(ABC):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def do_something(self):
        pass

class B(AbstractClassExample):
    pass            # No abstract methods implemented

class C(AbstractClassExample):
    def do_something(self):
        return self.value + 42


class AbstractClassExample(ABC):

    @abstractmethod
    def do_something(self):
        print("Some implementation!")


class AnotherSubclass(AbstractClassExample):
    def do_something(self):
        super().do_something()
        print("The enrichment from AnotherSubclass")


x = AnotherSubclass()
x.do_something()