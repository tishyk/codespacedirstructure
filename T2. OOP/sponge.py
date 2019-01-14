import random

class Sponge():
    def __init__(self):
        self.color = random.randint(0,10)
        self.state = 'clean'

    def set_color(self, color):
        print("Set sponge color")
        self.color = color

class Painter:
    color = 0

    def set_color(self, color):
        print("Set {} painter color".format(color))
        self.color = color

class SpongeFactory(Painter,Sponge):
    produced_count = 0

    def __init__(self, count):
        self.sponge_count = count
        self.sponges = []

    def set_color(self, color):
        print("Set factory color {}".format(color))
        Painter().set_color(color)
        for sponge in range(self.sponge_count):
            sponge = Sponge()
            sponge.set_color(color)
            # increase sponge factory produced count
            self.sponges.append(sponge)

spf = SpongeFactory(10)
spf.set_color(2)