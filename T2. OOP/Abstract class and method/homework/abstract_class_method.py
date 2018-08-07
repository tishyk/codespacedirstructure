from abc import ABC, abstractmethod
# Create abstract class for a ui from chat.gif


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