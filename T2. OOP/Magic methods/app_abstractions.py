# Application Abstractions

from abc import ABC, abstractmethod
from weakref import WeakKeyDictionary


class ABCConnection(ABC):
    @abstractmethod
    def __init__(self, address, port='22', **kwargs):
        self.connected = False
        self.address = address
        self.port = port
        self.connection_type = self.__class__.__name__
        self.user = ''
        self.rank = 0
        self.__dict__.update(kwargs)

    @abstractmethod
    def call(self, cmd):
        # connection call method realization
        pass

    @abstractmethod
    def check_call(self, cmd, timeout=60):
        # connection call method realization
        pass

    @abstractmethod
    def check_output(self, cmd, timeout=60):
        # connection call method realization
        pass

    @abstractmethod
    def connect(self):
        # Connection via supported connection type
        pass

    @abstractmethod
    def close_connection(self):
        # Close supported connection type
        pass

    @abstractmethod
    def wait_for_connection(self, timeout, polling=0.1):
        # connection call method realization
        pass

    @abstractmethod
    def is_alive(self):
        # check connection created and is alive
        pass


class ABCConnectionManager(ABC):
    connections = WeakKeyDictionary()    # Store all created connections

    @abstractmethod
    def create_ssh(self, *args, **kwargs):
        """Create ssh connection objects. Multiple sessions supported"""
        pass

    @abstractmethod
    def create_ftp(self, *args, **kwargs):
        # create ftp connection
        pass

    @abstractmethod
    def create_serial(self, *args, **kwargs):
        # create serial connection. Multiple session are not supported
        pass

    @abstractmethod
    def create_telnet(self, *args, **kwargs):
        # create telnet connection
        pass
