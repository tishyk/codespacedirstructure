"""Implementation of the state pattern"""
# http://www.radiostation.ru/know/range.html
import itertools


class Radio:
    """A radio.
    It has a scan button, and an AM/FM toggle switch."""

    def __init__(self):
        """We have an AM state and an FM state"""
        self.amstate = "Am"
        self.fmstate = "Fm"
        self.state = "Am"
        self.am_stations = itertools.cycle(["1250", "1380", "1510"])
        self.fm_stations = itertools.cycle(["81.3", "89.1", "103.9"])

    def toggle_amfm(self):
        if self.state == "Am":
            print("Switching to FM")
            self.state = "Fm"
        elif self.state == "Fm":
            print("Switching to AM")
            self.state = "Am"

    def scan(self):
        if self.state == "Am":
            print("Scanning... Station is", self.am_stations.__next__(),self.state)
        elif self.state == "Fm":
            print("Scanning... Station is", self.fm_stations.__next__(), self.state)


def main():
    ''' Test our radio out '''
    radio = Radio()
    actions = ([radio.scan] * 2 + [radio.toggle_amfm] + [radio.scan] * 2) * 2
    for action in actions:
        action()


if __name__ == '__main__':
    main()
"""
Scanning... Station is 1250 Am
Scanning... Station is 1380 Am
Switching to FM
Scanning... Station is 81.3 Fm
Scanning... Station is 89.1 Fm
Scanning... Station is 103.9 Fm
Scanning... Station is 81.3 Fm
Switching to AM
Scanning... Station is 1510 Am
Scanning... Station is 1250 Am
"""

# Add LW and TV frequency states

class State:
    """Base state. This is to share functionality"""

    def scan(self):
        """Scan the dial to the next station"""
        pass


class AmState(State):
    def __init__(self, radio):
        # radio, stations, name, toggle_amfm
        pass


class FmState(State):
    def __init__(self, radio):
        # radio, stations, name, toggle_amfm
        pass
