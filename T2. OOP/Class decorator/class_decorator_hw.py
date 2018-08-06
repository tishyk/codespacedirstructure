import random
import string
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s: %(levelname)s: %(message)s', datefmt="%b %d %H:%M:%S")

# Create User class with variables wrapped by property decorator,
# User class is a parent of UserView class. (username, user_id, status, user_device (PC, Android, Mac ..), last joining etc.)
# create username getter, setter and deleter property decorator methods
# Chat window get from chat.gif


def user_view(cls):

    # class decorator for User class
    # add class variable ip_address

    class UserView:
        def __init__(self, *args):
            self.wrapped = cls(*args)

        def __getattr__(self, name):
            return getattr(self.wrapped, name)

        setattr(cls, 'ip_address', None)

    return UserView


@user_view
class User(object):
    @property
    def username(self):
        return self.__get_username()

    @username.setter
    def username(self, name):
        self.__get_username = lambda: name

    @username.deleter
    def username(self):
        self.__get_username = lambda: ''

    def __get_username(self):
        """ :return: str, Chooses k unique random elements from a population sequence or set. """
        return "".join(random.sample(string.ascii_letters, random.randint(3,15)))


class UserView(User):

    @property
    def user_id(self):
        return random.randint(0, 1000000)

    @property
    def status(self):
        return None

    @property
    def user_device(self):
        return None

user = User()
logging.info(user.username)
logging.info(user.ip_address)
user_view = UserView()
logging.info("\n\n\n")
logging.info(user_view.user_id)
logging.info(user_view.ip_address)
logging.info(user_view.status)
