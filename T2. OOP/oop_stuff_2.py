import pprint


class Person:
    """Docstring"""
    my_age = 24 # class variable

    def __init__(self, name, age, *args, **kwargs):
        self.name = name # object variable
        self.age = age
        self.args = args
        self.kwargs = kwargs
        self.__strong = 100

    @property
    def strong(self):
        print('Strong person: {}'.format(self.__strong))
        return self.__strong

    def __call__(self, age):
        self.age = age
        print(self.age)

person = Person("John", 30)
print(person.__dict__)
print(Person.__name__, person.__doc__)
person.last = "Last"
setattr(person, "second", "John2")
pprint.pprint(person.__dict__)
obj_lst = (Person("Carl",20), Person("Jack",20))
lst = [setattr(obj, "on_click", "Carl") for obj in obj_lst]
print(obj_lst[0].name)
