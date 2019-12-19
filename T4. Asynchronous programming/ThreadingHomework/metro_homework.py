import time
import datetime
import random
import itertools
from threading import Thread, RLock

METRO_LINES = {"green": "green_stations.txt",
               "blue": "blue_stations.txt",
               "red": "red_stations.txt"}
TRANSFERS = (("Палац спорту", "Площа Льва Толстого"),
             ("Золоті ворота", "Театральна"),
             ("Майдан Незалежності", "Хрещатик"))

metro_open_time = datetime.time(6, 15)
metro_close_time = datetime.time(23, 59)
mr_lock = RLock()


def load_stations(metro_line):
    with open(METRO_LINES[metro_line], "r", encoding="utf8") as f:
        return f.read().splitlines()


class MrRider(Thread):
    def __init__(self, metro_line):
        name = f"Mr.{metro_line.title()}"
        Thread.__init__(self, name=name)
        self.stations_list = load_stations(metro_line)
        self.curr_station = None

    def run(self):
        # [1, 2, 3, 4, 5] -> [1, 2, 3, 4, 5, 4, 3, 2]
        stations_list = self.stations_list + self.stations_list[-2:-len(self.stations_list):-1]
        while True:
            curr_time = datetime.datetime.now().time()
            if metro_open_time < curr_time < metro_close_time:
                print(f"Metro is opened - {self.name} goes to ride.")
                self.ride(stations_list)

    def ride(self, stations_list):
        for station in itertools.cycle(stations_list):
            self.curr_station = station
            # with mr_lock:
            #     print(f"==={self.name} is on {station}===")
            self.check_for_friend(station)
            curr_time = datetime.datetime.now().time()
            if curr_time < metro_open_time or curr_time > metro_close_time:
                print(f"Metro is closed - {self.name} goes to sleep until its opening.")
                break
            time.sleep(random.choice((0.8, 0.12, 0.2)))

    def check_for_friend(self, station):
        with mr_lock:
            for transfer in TRANSFERS:
                if station in transfer:
                    print(f"{self.name} is on {station} (transfer station) at {datetime.datetime.now().time()}.")
                    for mr in mr_list:
                        if mr is not self and mr.curr_station in transfer:
                            print(f"{self.name} says hello to {mr.name}!!!!!!!!!!!!!!!!!!!!")


mr_list = [MrRider("green"), MrRider("blue"), MrRider("red")]
for mr in mr_list:
    mr.start()
