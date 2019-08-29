# Application Connections

import getpass
from app_abstractions import ABCConnection
from app_descriptors import IP_Descriptor

class Serial(ABCConnection):
    pass

class Serial232(ABCConnection):
    pass

class Telnet(ABCConnection):
    pass

class AppServer(ABCConnection):
    pass

class FTP(ABCConnection):
    pass

class SSH(ABCConnection):
    address = IP_Descriptor('address')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rank = 10

    def call(self, cmd):
        # connection call method realization
        pass

    def check_call(self, cmd, timeout=60):
        # connection call method realization
        pass

    def check_output(self, cmd, timeout=60):
        # connection call method realization
        pass

    def connect(self):
        # Connection via supported connection type
        #password = getpass.getpass()
        # create connection to host
        self.connected = True

    def close_connection(self):
        # Close supported connection type
        pass

    def wait_for_connection(self, timeout, polling=0.1):
        # connection call method realization
        pass

    def is_alive(cls):
        # check connection created and is alive
        pass

if __name__ == "__main__":
    # For ssh object testing
    ssh = SSH('10.124.198.24')
    print(ssh.address) # ssh.connect()
    ssh.address = '10.204.198.167'
    ssh.connect()
    ssh.address = '10.204.198.167'
