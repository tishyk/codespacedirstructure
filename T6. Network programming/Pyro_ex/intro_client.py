# saved as greeting-client.py
import Pyro4

uri = input("What is the Pyro uri of the greeting object? ").strip()
name = input("What is your name? ").strip()

greeting_maker = Pyro4.Proxy(uri)         # get a Pyro proxy to the greeting object
print(greeting_maker.get_fortune(name))   # call method normally



# python greeting-client.py
# What is the Pyro uri of the greeting object?  <<paste the uri that the server printed earlier>>
# What is your name?  <<type your name; in my case: Irmen>>
# Hello, Irmen. Here is your fortune message:
# Behold the warranty -- the bold print giveth and the fine print taketh away.
