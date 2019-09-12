"""
Allow an object to alter its behavior when its internal state changes.
The object will appear to change its class.
"""

import abc


class State(metaclass=abc.ABCMeta):
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the Context.
    """

    @abc.abstractmethod
    def request_handler(self):
        pass


class Context:
    """
    Define the interface of interest to clients.
    Maintain an instance of a ConcreteState subclass that defines the
    current state.
    """

    def __init__(self, state: State):
        # Save initial context state
        self.state = state

    def request(self):
        """ Call handle method of declared state object"""
        self.state.request_handler()

    def change_state(self, state: State) -> None:
        """Changing context object state to any context states"""
        assert isinstance(state, State), "State object not recognized"
        self.state = state


class ConcreteStateA(State):
    """
    Implement a behavior associated with A state of the Context.
    """

    def request_handler(self) -> None:
        """Context handle method for state A"""
        print('Actions for context state A')


class ConcreteStateB(State):
    """
    Implement a behavior associated with B state of the Context.
    """

    def request_handler(self) -> None:
        """Context handle method for state B"""
        print('Actions for context state B')


def main():
    concrete_state_a = ConcreteStateA()
    concrete_state_b = ConcreteStateB()

    context = Context(concrete_state_a)
    context.request()  # Action from state A
    context.change_state(concrete_state_b)
    context.request()  # Action from state B


if __name__ == "__main__":
    main()
