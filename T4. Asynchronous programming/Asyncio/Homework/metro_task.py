import itertools
import datetime
import random
import time
from math import sqrt
import queue
import collections
import asyncio


class Metro():
    stations_opening = datetime.time(5, 45, 0)
    stations_closing = datetime.time(23, 50, 0)

    red_train_speed = random.choice((0.02, 0.03, 0.04))
    blue_train_speed = random.choice((0.1, 0.2, 0.3))
    green_train_speed = random.choice((0.8, 0.9, 1))

    red_station = ""
    blue_station = ""
    green_station = ""


def read_stations(path):
    """Yield station with as soon as train_speed can do this"""
    with open(path, encoding='utf8') as fileline:
        yield from (line.strip() for line in fileline.readlines())


async def red_train(mr_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        Metro.red_station = station
        await asyncio.sleep(Metro.red_train_speed)
        if station == "Театральна" and Metro.green_station == "Золоті ворота":
            print(f"{mr_name} ==> Mr.Green, ({station}:{Metro.green_station})")
        elif station == "Хрещатик" and Metro.blue_station == "Майдан Незалежності":
            print(f"{mr_name} ==> Mr.Blue, ({station}:{Metro.blue_station})")


async def blue_train(mr_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        Metro.blue_station = station
        await asyncio.sleep(Metro.red_train_speed)
        if station == "Майдан Незалежності" and Metro.red_station == "Хрещатик":
            print(f"{mr_name} ==> Mr.Red, 'Hello Bro' ({station}:{Metro.red_station})")
        elif station == "Площа Льва Толстого" and Metro.green_station == "Палац спорту":
            print(f"{mr_name} ==> Mr.Green, ({station}:{Metro.green_station})")


async def green_train(mr_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        Metro.green_station = station.strip()
        await asyncio.sleep(Metro.red_train_speed)
        if station == "Палац спорту" and Metro.blue_station == "Площа Льва Толстого":
            print(f"{mr_name} ==> Mr.Blue, ({station}:{Metro.blue_station})")
        elif station == "Золоті ворота" and Metro.red_station == "Театральна":
            print(f"{mr_name} ==> Mr.Red, ({station}:{Metro.red_station}")


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    red_task = ioloop.create_task(red_train('Mr.Red', "red_stations.txt"))
    green_task = ioloop.create_task(green_train('Mr.Green', 'green_stations.txt'))
    blue_task = ioloop.create_task(blue_train('Mr.Blue', 'blue_stations.txt'))
    ioloop.run_until_complete(asyncio.wait([red_task, green_task, blue_task]))
    ioloop.close()
