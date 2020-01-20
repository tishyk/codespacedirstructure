import sys
import abc

sprite = "loaded_img"

class Canvas():
    def add_particle(self, particle):
        pass


class ABCGame(metaclass=abc.ABCMeta):
    canvas = Canvas()

    def game_setup(self):
        pass

    def addParticle(self, particle):
        print('add particle')

    def draw(self, canvas):
        print('Show canvas')


class WinGame(ABCGame):
    particles = []
    conf = ""

    def game_setup(self):
        pass

    def addParticle(self, particle):
        print('add particle')

    def draw(self, canvas):
        print('Show canvas')


class LinuxGame((ABCGame)):
    particles = []
    conf = ""

    def game_setup(self):
        pass

    def addParticle(self, particle):
        print('add particle')

    def draw(self, canvas):
        print('Show canvas')


class MacGame((ABCGame)):
    particles = []
    conf = ""

    def game_setup(self):
        pass

    def addParticle(self, particle):
        print('add particle')

    def draw(self, canvas):
        print('Show canvas')


class Particle:
    coords = 0, 0
    vector = (0, 0), (0, 0)
    speed = 0
    color = "#f055af15"

    def move(self, coords, speed):
        pass
        print('Move to other place')

    def draw(self):
        pass

    def get_sprite(self):
        return sprite




class AbsractGame:
    def __init__(self):
        if sys.platform == 'win32':
            self.game = WinGame()
        elif sys.platform == 'linux':
            self.game = LinuxGame()
        elif sys.platform == 'darwin':
            self.game = MacGame()
        self.load_game_config()
        canvas = Canvas()

    def load_game_config(self):
        self.game.game_setup()
        # bins_loader()
        # verify()
        # conf_load()
        pass

    def run(self):
        imgs_lst = [Particle() for p in range(50)]
        for p in imgs_lst:
            self.game.canvas.add_particle(p)
        while True:
            self.game.canvas.add_particle()
            self.game.draw(self.game.canvas)
            canvas = self.game.canvas


if __name__ == "__main__":
    game = AbsractGame()
    game.run()
