#! usr/bin/python
import random
import string
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s: %(levelname)s: %(message)s', datefmt="%b %d %H:%M:%S")

# Create User class with variables wrapped by property decorator,
# User class is a parent of UserView class. (username, user_id, status, user_device (PC, Android, Mac ..), last joining etc.)
# create username getter, setter and deleter property decorator methods
# Chat window get from chat.gif


def userview(cls):
    class UserView(object):
        @classmethod
        def generate_ip_address(self):
            return ".".join([str(random.randrange(0, 255 ,3)) for x in range(0, 4)])

        def __init__(self, *args):
            self.user_view = cls(*args)
            print(f"Created {self.user_view} from passed {cls}: {dir(self.user_view)}")
            self.user_view.ip_address = self.generate_ip_address()
            print(f"After assigning ip_address: {dir(self.user_view)}")

        def __getattr__(self, name):
            print(f"{self} getting attribute {name}")
            return getattr(self.user_view, name)

        # class decorator for User class
        # add class variable ip_address
    return UserView

@userview
class User:
    def __init__(self):
        self._username = None

    @property
    def username(self):
        if not self._username:
            self._username = self.__get_username()
        return self._username

    def __get_username(self):
        """ :return: str, Chooses k unique random elements from a population sequence or set. """
        return "".join(random.sample(string.ascii_letters, random.randint(3,15)))

    @username.setter
    def username(self, value):
        print(f"Setting username with '{value}'")
        self._username = value

    @username.deleter
    def username(self):
        print("Deleting username")
        self._username = ''

    # user_device property implemented in Slots/homework/slot_hw.py file



user = User()
#logging.info(str(help(user)))
logging.info(user.username)
user.username = "newUserName"
logging.info(user.username)
del(user.username)
logging.info(f"User ip_address: {user.ip_address}")
logging.info(user.username)


