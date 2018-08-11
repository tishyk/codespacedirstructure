import random
from abstract_drive_power import Observer
from decorators import retry_decorator


class CGEMHDDrive(Observer):

    allowed_commands = ['on', 'off', 'reset', 'blink']

    def __init__(self, drive_name, *args, **kwargs):
        self.drive_name = drive_name

    def __getattr__(self, attr_name):
        print("Command ignored. " + self.get_info_message())
        return self.get_info_message

    def get_info_message(self):
        return "Allowed commands are: %s" % self.allowed_commands

    @property
    def __response_code(self):
        return random.randint(0, 1)

    @retry_decorator
    def on(self):
        print('On command is executed for disk with name %s' % self.drive_name)
        return self.__response_code

    @retry_decorator
    def off(self):
        print('Off command is executed for disk with name %s' % self.drive_name)
        return self.__response_code

    @retry_decorator
    def reset(self):
        print('Reset command is executed for disk with name %s' % self.drive_name)

        return self.__response_code

    @retry_decorator
    def blink(self):
        print('Blink drive is executed for disk with name %s' % self.drive_name)
        return self.__response_code
