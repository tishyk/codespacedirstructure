import random
import time
import threading

class Track:
    def __init__(self, available_places):
        self.car_number = available_places
        self.cars = []
        self.distance = 1000
        self.overtaking_possibility = lambda: random.choice((True, False))
        self.leader_board = []
        self.board = threading.Lock()
        self.green_light = threading.Event()
        self.track_lanes = threading.Semaphore(2)

    def add_car(self, car):
        assert isinstance(car, RaceCar), "Not a RaceCar instance"
        self.cars.append(car)

    def set_cars_on_track(self):
        for car in self.cars:
            car.start()

    def run_race(self):

        start_time = time.time()
        self.green_light.set()

        while any(car.is_alive() for car in self.cars):  # threading.enumerate()
            for car in self.cars:
                car.change_speed(100)  # random.randrange(0, 350))
                if self.overtaking_possibility():
                    self.track_lanes._value = random.randrange(1, 10)
        print("Last car arrived at:", time.time() - start_time)
        print(f"Leader cars : {self.leader_board[:3]}")


class RaceCar(threading.Thread):
    def __init__(self, car, track):
        self.car = car
        self.speed = 0
        self.track = track
        self.distance = track.distance
        super().__init__()
        self.is_alive()

    def run(self):
        print("Waiting for green light to start the race..")
        self.track.green_light.wait()

        while self.distance > 0:
            self.track.track_lanes.acquire()
            print(f'{self.distance} km to go. Car "{self.car}" overtaking speed is {self.speed}km/h.')
            #time.sleep(0.2)  # time
            self.distance -= self.speed  # * 1 time unit
            self.track.track_lanes.release()
        with self.track.board:
            self.track.leader_board.append(self.car)
        print(f"Car {self.car} finished race")

    def change_speed(self, speed):
        self.speed = speed



if __name__ == "__main__":
    track = Track(10)
    race_cars = [RaceCar(num, track) for num in range(track.car_number)]
    for car in race_cars:
        track.add_car(car)
    track.set_cars_on_track()
    track.run_race()



