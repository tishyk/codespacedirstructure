# A power manager construction can be found bellow.
# 1. Need to remove redundant code LS_POWER_COMMAND is a only one cmd needed
# 2. Create an observable class - CHHPowerMgr that can send command to CGEMHDDrive(observer) class
# 3. Add known actions for observer class - off, on, reset, blink_drive, ignore any other msgs.
# 4. implement off, on, reset, blink_drive methods that will used for CHHPowerMgr request(send_command)
# 5*. import random and use random return code for above methods (0:Success, 1:Failed)
# 6**. implement __getattr__(__get__), decorator for methods return code validation.
#  In case of failed rc retry method was called for 3 times. Return final rc

from abstract_drive_power import Observable
from cgemhdd_drive import CGEMHDDrive


class CHHPowerMgr(Observable):

    def add_shh_client(self, shh_client):
        assert isinstance(shh_client, CGEMHDDrive), "Only CGEMHDDrive object are available for adding"
        if shh_client not in self.shh_clients:
            self.shh_clients.append(shh_client)
            print("SHH client added")

    def request(self, send_command):
        assert isinstance(send_command, str), "Send command should have 'str' type"
        for ssh_client in self.shh_clients:
            getattr(ssh_client, send_command)()
