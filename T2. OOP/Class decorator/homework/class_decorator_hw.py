#! usr/bin/python
import random
import string
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s: %(levelname)s: %(message)s', datefmt="%b %d %H:%M:%S")

# Create User class with variables wrapped by property decorator,
# User class is a parent of UserView class. (username, user_id, status, user_device (PC, Android, Mac ..), last joining etc.)
# create username getter, setter and deleter property decorator methods
# Chat window get from chat.gif


class User:
    @property
    def username(self):
        return self.__get_username()

    def __get_username(self):
        """ :return: str, Chooses k unique random elements from a population sequence or set. """
        return "".join(random.sample(string.ascii_letters, random.randint(3,15)))

def userview(cls):
    def UserView():
        pass
    # class decorator for User class
    # add class variable ip_address
    return UserView

user = User()
logging.info(user.username)