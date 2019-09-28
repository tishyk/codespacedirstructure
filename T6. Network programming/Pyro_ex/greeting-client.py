# saved as greeting-client.py
from Pyro5.api import Proxy

name = input("What is your name? ").strip()

greeting_maker = Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
print(greeting_maker.get_fortune(name))
