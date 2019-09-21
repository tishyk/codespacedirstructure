import datetime
import time
import itertools
import random
import threading

lock = threading.Lock()
stations_opening = datetime.time(5, 45, 0)
stations_closing = datetime.time(23, 50, 0)

red_train_speed = random.choice((0.1, 0.2, 0.3))
blue_train_speed = random.choice((0.1, 0.15, 0.2))
green_train_speed = random.choice((0.8, 0.12, 0.2))

hour_min_now = lambda: "{}:{}:{}".format(time.localtime().tm_hour,
                                         time.localtime().tm_min,
                                         time.localtime().tm_sec)

print("We are started at {}".format(hour_min_now()))

intersections = ("Золоті ворота", "Театральна", "Майдан Незалежності",
                 "Хрещатик", "Площа Льва Толстого", "Палац спорту")


def generate_stations(station_file):
    with open(station_file, encoding='utf8') as line:
        stations = [station.strip() for station in line.readlines()]
    one_station_cycle = itertools.chain(stations, stations[::-1])
    for station in itertools.cycle(one_station_cycle):
        yield station


class RedLine(threading.Thread):
    intersection = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for station in generate_stations('red_stations.txt'):
            # print("We are on {} station at {}:{}:{}".format(station, *hour_min_now()))
            if station in intersections:
                with lock:
                    self.__class__.intersection = True
                    if BlueLine.intersection:
                        print("Hello from Mr.Red to Mr.Blue at {}".format(
                            hour_min_now()))
                    elif GreenLine.intersection:
                        print("Hello from Mr.Red to Mr.Green at {}".format(
                            hour_min_now()))
                    self.__class__.intersection = True
            else:
                self.__class__.intersection = False
            time.sleep(red_train_speed)


class BlueLine(threading.Thread):
    intersection = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for station in generate_stations('blue_stations.txt'):
            # print("We are on {} station at {}:{}:{}".format(station, *hour_min_now()))
            if station in intersections:
                with lock:
                    self.__class__.intersection = True
                    if RedLine.intersection:
                        print("Hello from Mr.Blue to Mr.Red at {}".format(hour_min_now()))
                    elif GreenLine.intersection:
                        print("Hello from Mr.Blue to Mr.Green at {}".format(hour_min_now()))
            else:
                self.__class__.intersection = False
            time.sleep(blue_train_speed)


class GreenLine(threading.Thread):
    intersection = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for station in generate_stations('green_stations.txt'):
            # print("We are on {} station at {}:{}:{}".format(station, *hour_min_now()))
            if station in intersections:
                with lock:
                    self.__class__.intersection = True
                    if BlueLine.intersection:
                        print("Hello from Mr.Green to Mr.Blue at {}".format(hour_min_now()))
                    elif RedLine.intersection:
                        print("Hello from Mr.Green to Mr.Red at {}".format(hour_min_now()))
            else:
                self.__class__.intersection = False
            time.sleep(green_train_speed)


redline_train = RedLine()
blueline_train = BlueLine()
greenline_train = GreenLine()

redline_train.start()
blueline_train.start()
greenline_train.start()
