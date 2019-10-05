import itertools
import datetime
import random
import time
from math import sqrt
import queue
import collections
import asyncio

stations_opening = datetime.time(5, 45, 0)
stations_closing = datetime.time(23, 50, 0)

red_train_speed = random.choice((0.1, 0.2, 0.3))
blue_train_speed = random.choice((0.1, 0.15, 0.2))
green_train_speed = random.choice((0.8, 0.12, 0.2))
red_station = ""
blue_station = ""
green_station = ""


class Task:
    """ Aggregates a coroutine and integer id """
    next_id = 0

    def __init__(self, routine):
        self.id = Task.next_id
        Task.next_id += 1
        self.routine = routine


class Scheduler:
    def __init__(self):
        self.executable_tasks = collections.deque()
        self.completed_task_results = {}
        self.failed_task_error = {}

    def add(self, routine):
        task = Task(routine)
        self.executable_tasks.append(task)
        return task.id

    def run_until_complete(self):
        while len(self.executable_tasks) != 0:
            task = self.executable_tasks.popleft()
            #            print("Running task {} ... ".format(task.id), end='')
            try:
                yielded = next(task.routine)
            except StopIteration as stopped:
                print("completed with result: {!r}".format(stopped.value))
                self.completed_task_results[task.id] = stopped.value
            except Exception as exec:
                print("failed with exception: {}".format(exec))
            else:
                assert yielded is None
                #                print('now yielded')
                self.executable_tasks.append(task)


def read_stations(path):
    """Yield station with as soon as train_speed can do this"""
    with open(path, encoding='utf8') as line:
        return [station.strip() for station in line.readlines()]


def red_train(task_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        yield from async_sleep(red_train_speed)
        global red_station; red_station = station
        if station == "Театральна" and green_station == "Золоті ворота":
            print("Red = Green, %s - %s" % (station, green_station))
        elif station == "Хрещатик" and blue_station == "Майдан Незалежності":
            print("Red = Blue, %s - %s" % (station, blue_station))
        yield


def blue_train(task_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        yield from async_sleep(red_train_speed)
        global blue_station; blue_station = station
        if station == "Майдан Незалежності" and red_station == "Хрещатик":
            print("Blue = Red, %s - %s" % (station, red_station))
        elif station == "Площа Льва Толстого" and green_station == "Палац спорту":
            print("Blue = Green, %s - %s" % (station, green_station))
        yield


def green_train(task_name, station_file_path):
    stations = read_stations(path=station_file_path)
    for station in itertools.cycle(stations):
        yield from async_sleep(red_train_speed)
        global green_station; green_station = station
        if station == "Палац спорту" and blue_station == "Площа Льва Толстого":
            print("Green = Blue, %s - %s" % (station, blue_station))
        elif station == "Золоті ворота" and red_station == "Театральна":
            print("Green = Red, %s - %s" % (station, red_station))
        yield


def async_sleep(interval):
    start = time.time()
    expiry = start + interval
    while True:
        yield
        now = time.time()
        if now >= expiry:
            break


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.add(red_train('Mr.Red', "red_stations.txt"))
    scheduler.add(blue_train('Mr.Blue', 'blue_stations.txt'))
    scheduler.add(green_train('Mr.Green', 'green_stations.txt'))
    scheduler.run_until_complete()
