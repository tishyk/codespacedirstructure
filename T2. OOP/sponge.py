import random

class Sponge():
    def __init__(self):
        self.color = random.randint(0,10)
        self.state = 'clean'

    def set_color(self, color):
        print(f"Sponge set_color {self}")
        print(f"Set sponge color {color}")
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
            print(f"Created Sponge {sponge} with default color {sponge.color}")
            super(Painter, self).set_color(color) # TODO:  Q: Не можу розібратись як ця стрічка коду (показана на занятті) може заміняти наступну (закоментовану). Додав прінти і бачу, що колір який ми додаємо у sponges не змінений, а лишається автозгенерованим (тобто цей рядок і наступний не є еквівалентними). Допоможіть, будь ласка, розібратись.
            # sponge.set_color(color)
            # increase sponge factory produced count
            self.__class__.produced_count += 1 # З цією все зрозуміло
            self.sponges.append(sponge)
            print(f"SpongeFactory: sponge {sponge}, color {sponge.color}")
            print("+" * 20)

spf = SpongeFactory(10)
spf.set_color(2)
