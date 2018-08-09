from abc import ABC, abstractmethod


class ObservableInterface(ABC):
    @abstractmethod
    def register(self, observer):
        # Add observer to known observers
        pass

    @abstractmethod
    def unregister(self, observer):
        # remove observer from known obseervers
        pass

    @abstractmethod
    def unregister_all(self):
        pass

    @abstractmethod
    def send_update(self, *args, **kwargs):
        # Send updates to registered observers
        pass


class ObserverInterface(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        # method to get updates from Subject
        pass
