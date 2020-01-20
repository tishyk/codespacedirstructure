import random


class RaceCar():
    def __init__(self, color):
        self.color = color
        self.__driver_name = "John"

    @property
    def driver(self):
        return self.__driver_name

    @driver.setter
    def driver(self, value):
        self.__driver_name = value




rc = RaceCar('red')
rc.driver
rc.driver = 140
rc.driver
print(rc.driver)

#
#
# class Van():
#     def __init__(self, color):
#         self.color = color
#
#
# class Jeep():
#     def __init__(self, color):
#         self.color = color
#
#
# class CarDriver():
#     def __new__(cls, *args, **kwargs):
#         car = random.choice((RaceCar, Van, Jeep))
#         cls.car = car(kwargs.get('color', 'white'))
#         return super().__new__(cls)
#
#     def __init__(self, name, *args, **kwargs):
#         self.name = name
#         print("Object of {} created".format(self.__class__.__name__))
#
#
# cd1 = CarDriver(name="John", color='red')
# cd2 = CarDriver(name="Smith")
# print(cd1.car)
#
# # class MyClass():
# #     def __new__(cls, *args, **kwargs):
# #         if all((('A' in arg or 'B' in arg) for arg in args)):
# #             return super().__new__(cls)
# #         else:
# #             return object
# #
# #     def __init__(*args, **kwargs):
# #         print("Object created")
# #
# #
# # mc1 = MyClass("A") #--> MyClass
# # mc2 = MyClass("A", "B") #--> MyClass
# # not_mc1 = MyClass("C") #--> object
# # not_mc2 = MyClass("B", "C") #--> object
