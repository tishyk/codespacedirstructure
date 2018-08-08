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
    
    def __init__(self):
        self._x = '11'

    @property
    def username(self):
        return self._x#'11'#self.__get_username()

    @username.setter
    def username(self,name):
        self._x = name

    @username.deleter
    def username(self):
        print('Username was deleted')
        self._x = None


def userview(cls):
    def UserView():
        pass
    # class decorator for User class
    # add class variable ip_address
    return UserView

user = User()
# print(user.username)
user.username = 'adf'
logging.info(user.username)
del user.username
logging.info(user.username)