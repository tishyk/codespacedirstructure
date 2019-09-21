import time
import itertools
import random
import threading

TIME_NOW = lambda: time.strftime("%H:%M:%S")


class FriendThread(threading.Thread):
    intersection = False
    train_speed = random.random() / 10  # station changing speed 0..1
    rlock = threading.RLock()

    def __init__(self, thread_name, station_file_path):
        self.full_name = thread_name
        threading.Thread.__init__(self, name=thread_name)
        self.friends = []  # store friends to say hello
        self.station_file_path = station_file_path
        self.intersection_points = ()
        self.intersection_point = 0
        self.shortly = None
        self.hello_string = lambda name: "Hello {} said {} at {}".format(name, thread_name, TIME_NOW())

    def stations(self):
        """Yield station with as soon as train_speed can do this"""
        with open(self.station_file_path, encoding='utf8') as line:
            stations = [station.strip() for station in line.readlines()]
        one_station_cycle = itertools.chain(stations, stations[::-1])
        for station in itertools.cycle(one_station_cycle):
            # Caution! <generator object ThreadLine.stations.<locals>.<genexpr> at 0x028FF6C0>  can be obtained here
            # in case of stations will be a generator
            with self.rlock:
                self.intersection_point = 0
            yield station

    def add_friend(self, friend):
        """Register friend and self as a friend list in obtained friend"""
        if friend not in self.friends:
            self.friends.append(friend)
            if self not in friend.friends:
                print("{} and {} is a friends now".format(self.full_name, friend.full_name))
            friend.add_friend(self)

    def say_hello(self):
        with self.rlock:
            """RLock for outer intersection value"""
            for friend in self.friends:
                if self.intersection_point and friend.intersection_point == self.intersection_point:
                    print(self.hello_string(friend.full_name))

    def run(self):
        print("\tA story of my friend named {} starts from going to metro station..".format(self.full_name))
        for station in self.stations():
            # if not self.shortly:
            # print("\t- {} on {} station at {}".format(self.full_name, station, TIME_NOW()))
            if station in self.intersection_points:
                # RLock for inner intersection value
                with self.rlock:
                    self.intersection_point = self.intersection_points[station]
                    self.say_hello()
            time.sleep(self.train_speed)


if __name__ == "__main__":
    print("Friends story started at {}".format(TIME_NOW()))

    mr_red = FriendThread('Mr.Red', 'red_stations.txt')
    ms_blue = FriendThread('Ms.Blue', 'blue_stations.txt')
    mr_green = FriendThread('Mr.Green', 'green_stations.txt')

    mr_red.intersection_points = {"Театральна": 1, "Хрещатик": 2}
    ms_blue.intersection_points = {"Майдан Незалежності": 2, "Площа Льва Толстого": 3}
    mr_green.intersection_points = {"Золоті ворота": 1, "Палац спорту": 3}

    mr_red.add_friend(ms_blue)
    mr_red.add_friend(mr_green)
    ms_blue.add_friend(mr_green)

    mr_red.start()
    ms_blue.start()
    mr_green.start()

    time.sleep(0.002)
    mr_red.shortly = True
    ms_blue.shortly = True
    mr_green.shortly = True
