
# A power manager construction can be found bellow.
# 1. Need to remove redundant code LS_POWER_COMMAND is a only one cmd needed
# 2. Create an observable class - CHHPowerMgr that can send command to CGEMHDDrive(observer) class
# 3. Add known actions for observer class - off, on, reset, blink_drive, ignore any other msgs.
# 4. implement off, on, reset, blink_drive methods that will used for CHHPowerMgr request(send_command)
# 5*. import random and use random return code for above methods (0:Success, 1:Failed)
# 6**. implement __getattr__(__get__), decorator for methods return code validation.
#  In case of failed rc retry method was called for 3 times. Return final rc
'''
import time
from CExceptions import CSshExcn
from core.lib.testwarelogger import testlog


class CHDDPowerMgr(object):
    """
    CHDDPowerMgr - class to control disk power via ssh session and slot number.
    """
    CONTROLLER_TYPE = {'laguna_seca': 'Laguna Seca', 'talladega': 'SATI-TL'}
    CV_COMMAND = "dmidecode -s system-product-name - get storage controller ver"  # Controller version
    # LS_POWER_COMMAND format with "off" or "on" and slot number
    LS_POWER_COMMAND = r'/avid/tools/bin/gem_utils.py --mode=cli --clicommand="power{0}drive {1}"'
    TD_POWER_COMMAND = r'echo "power{0}drive {1}">/dev/ttyS1'
    LS_RESET_COMMAND = r'/avid/tools/bin/gem_utils.py --mode=cli --clicommand="resetdrive {}"'  # format with slot number
    TD_RESET_COMMAND = r'echo "resetdrive {}">/dev/ttyS1'  # format with slot number

    SERIAL_PORT_CONF = r"stty -F /dev/ttyS1 speed 115200 cread line 0 min 1 time 5 ignbrk -brkint " + \
                       "-icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke"
    TD_CONTROLLER = False

    def __init__(self, ssh_client):
        self.__ssh_client = ssh_client
        self.__disk_slot = None
        self.port_speed = "115200"

    @property
    def controller_type(self):
        """ Return str with host controller type(Ex. SATI-TL or Laguna Seca)"""
        try:
            return self.__ssh_client.check_output(self.CV_COMMAND)
        except CSshExcn:
            raise RuntimeError("Obtaining Controller Type Failed!")

    @property
    def power_command(self):
        """ Obtaining command for power off/on disk for specific controller type """
        if self.CONTROLLER_TYPE['laguna_seca'] in self.controller_type:
            power_command = self.LS_POWER_COMMAND
        elif self.CONTROLLER_TYPE['talladega'] in self.controller_type:
            power_command = self.TD_POWER_COMMAND
            self.TD_CONTROLLER = True
        else:
            raise AssertionError("Controller type not supported!")
        return power_command

    @property
    def reset_command(self):
        """ Obtaining command for reset disk for specific controller type """
        if self.CONTROLLER_TYPE['laguna_seca'] in self.controller_type:
            reset_command = self.LS_RESET_COMMAND
        elif self.CONTROLLER_TYPE['talladega'] in self.controller_type:
            reset_command = self.TD_RESET_COMMAND
            self.TD_CONTROLLER = True
        else:
            raise AssertionError("Controller type not supported!")
        return reset_command

    def __serial_port_setup(self):
        self.__ssh_client.call(self.SERIAL_PORT_CONF)  # First output has previous port settings
        port_speed = self.__ssh_client.check_output(self.SERIAL_PORT_CONF).strip()
        testlog.debug("Serial Port speed: {}!".format(port_speed))
        if port_speed != self.port_speed:
            raise RuntimeError("Serial port setup failed!")

    def power_on(self, slot=0):
        """ Send Power on command for disk drive.
           :param slot: Set number or left empty in case of previous call power_off method
        """
        if self.__disk_slot and not slot:
            slot = self.__disk_slot
        self.__serial_port_setup()
        testlog.info("Power on drive in slot {}!".format(slot))
        call = self.__ssh_client.call(self.power_command.format("on", slot))
        testlog.info('Return code {}'.format(call))
        if call:
            testlog.error(call)
        self.__disk_slot = None
        time.sleep(3)  # time for drive on with diskmanager service

    def power_off(self, slot, force=False):
        """  Send Power off command for disk drive.
        Cannot be powered off more than one drive!
        :param slot: Set number, no default value.
        :param force: bool, use in case power off one more drive
        """
        if self.__disk_slot and slot and not force:
            raise RuntimeError("Power on Slot {} before power off new Slot {}!".format(self.__disk_slot, slot))
        self.__serial_port_setup()
        testlog.info("Power off drive in slot {}!".format(slot))
        call = self.__ssh_client.call(self.power_command.format("off", slot))
        testlog.info('Return code {}'.format(call))
        if call:
            testlog.error(call)
        self.__disk_slot = slot

    def reset_drive(self, slot):
        """  Reset disk drive.
        :param slot: Set number, no default value.
        """
        self.__serial_port_setup()
        testlog.info("Reset drive in slot {}!".format(slot))
        call = self.__ssh_client.call(self.reset_command.format(slot))
        if call:
            testlog.error("Power reset failed! Get return code {}".format(call))
        time.sleep(10)  # time for drive reset with diskmanager service
'''