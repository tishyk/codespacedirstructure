import random
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s: %(levelname)s: %(message)s', datefmt="%b %d %H:%M:%S")


# Create User class with variables wrapped by property decorator,
# User class is a parent of UserView class. (username, user_id, status, user_device (PC, Android, Mac ..), last joining etc.)
# create username getter, setter and deleter property decorator methods
# Chat window get from chat.gif

def Userview(cls):
    class Wrapper(object):
        def __init__(self, *args):
            self.profile = cls(*args)
            self.profile._ip = '{}.{}.{}.{}'.format(*(random.randint(0, 255) for _ in range(4)))

        @property
        def username(self):
            return '{} {}'.format(self.profile._firstname, self.profile._lastname)

        @username.setter
        def username(self, _username):
            (self.profile._firstname, self.profile._lastname) = _username.split(' ') if (' ' in _username) else (
            _username, self.profile._lastname)

        @username.deleter
        def username(self):
            self.profile._firstname = 'Unknown'
            self.profile._lastname = 'Unknown'

    return Wrapper


@Userview
class User:
    def __init__(self, firstname='Unknown', lastname='Unknown', device='Unknown'):
        self._id = id(self)
        self._firstname = firstname
        self._lastname = lastname
        self._device = device

user = User('Oleksandr', 'Fishchenko')

# get property
logging.info(user.username)

# set property
user.username = 'John'
logging.info(user.profile.__dict__)
user.username = 'John Doe'
logging.info(user.profile.__dict__)

# delete property
del user.username
logging.info(user.profile.__dict__)
