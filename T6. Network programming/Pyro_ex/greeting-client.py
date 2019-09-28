# saved as greeting-client.py
import Pyro5

name = input("What is your name? ").strip()

greeting_maker = Pyro5.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
print(greeting_maker.get_fortune(name))
