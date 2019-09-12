"""
Use sharing to support large numbers of fine-grained objects
efficiently.
"""
import abc


class FlyweightFactory:
    """
    Create and manage flyweight objects.
    Ensure that flyweights are shared properly. When a client requests a
    flyweight, the FlyweightFactory object supplies an existing instance
    or creates one, if none exists.
    """

    def __init__(self):
        self._flyweights = {}

    def get_flyweight(self, key):
        try:
            flyweight = self._flyweights[key]
        except KeyError:
            flyweight = ConcreteFlyweight()
            self._flyweights[key] = flyweight
        return flyweight


class Flyweight(metaclass=abc.ABCMeta):
    """
    Declare an interface through which flyweights can receive and act on
    extrinsic state.
    """

    def __init__(self, intrinsic_state, path):
        self.intrinsic_state = intrinsic_state
        self.color = 'green'
        self.border = 2
        self.path = path

    @abc.abstractmethod
    def operation(self, x, y):
        # canvas.draw(self.path, x,y)
        pass


class ConcreteFlyweight(Flyweight):
    """
    Implement the Flyweight interface and add storage for intrinsic
    state, if any. A ConcreteFlyweight object must be sharable. Any
    state it stores must be intrinsic; that is, it must be independent
    of the ConcreteFlyweight object's context.
    """

    def __init__(self):
        self.color = 'green'
        self.path = 'img'
        self.border = 2

    def operation(self, x, y):
        # canvas.draw(self.path, x,y)
        pass


def main():
    flyweight_factory = FlyweightFactory()
    concrete_flyweight = flyweight_factory.get_flyweight("key")
    concrete_flyweight.operation(10, 15)


if __name__ == "__main__":
    main()
