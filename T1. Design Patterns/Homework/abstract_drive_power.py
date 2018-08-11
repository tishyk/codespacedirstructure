from abc import ABC, abstractmethod


class Observable(ABC):
    def __init__(self):
        self.shh_clients = []

    @abstractmethod
    def add_shh_client(self, shh_client):
        pass

    @abstractmethod
    def request(self, send_command):
        pass


class Observer(ABC):

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def blink(self):
        pass
