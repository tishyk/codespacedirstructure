"""Задача на переменные класса, объекта, property, class method, super method.

1. Создать класс Robot, Cat и RoboCat
2. В классе Robot нужно использовать только переменные класса.
3. В классе Cat нужно использовать только переменные объекта.
4. Класс RoboCat наследуется с классов Robot и Cat и переопределяет некоторые параметры.

Robot:
    region = str, sale_country (China, USA or Europe)
    id = int, class id()
    abilities - empty list
    
    serial_number - property, return str -> region(в нижнем регистре) + '_' + id
    save_ability - method, args: str and RoboCat object, add ability(str) into CAT skills list, save ability name into abilities, 
                          return True if object is RoboCat class object
    remove_ability - method, args: str and RoboCat object, add ability(str) into cat skills list, save ability name into abilities, 
                          return True if object is RoboCat had str ability                        
    
    
Cat:
    name - str, add to init method
    age - int, cat age, add to init
    bread - str,  choose any from list https://en.wikipedia.org/wiki/List_of_cat_breeds
    skills - list with str, list of cat abilities, can be empty list
    
    knowledge_level - property, return len of cat skills
    add_skill - method, arg: str add cat skill(str) into cat skills list, return True if arg was not known 
    forget_skill - method, arg: str remove cat skill(str) from cat skills, return True if arg was removed 
    
RoboCat:
    init - add cat name, age and cat bread
        choose robot region by cat bread
        abilities - empty list
        
    add_skill - method, arg: str, print received skill, check result of cat add_skill and robot save_ability
    remove_skill- method, arg: str, print received skill, check result of cat forget_skill and robot remove_ability
    sync* - method, no args: sync robot updates within all Robocats about known abilities (Robot variable can be used)
    
    sync** - method, no args: sync robot updates within all Robocats about known abilities (gc or weakref)
"""
import random

BREEDS = [
    "Abyssinian", "Aegean", "American Bobtail", "American Curl", "American Shorthair", "American Wirehair", "Aphrodite Giant",
    "Arabian Mau", "Asian", "Asian Semi-longhair", "Australian Mist", "Balinese", "Bambino", "Bengal", "Birman", "Bombay", "Brazilian Shorthair",
    "British Longhair", "British Semi-longhair", "British Shorthair", "Burmese", "Burmilla", "California Spangled", "Chantilly-Tiffany", "Chartreux",
    "Chausie", "Colorpoint Shorthair", "Cornish Rex", "Cymric", "Cyprus", "Devon Rex", "Donskoy or Don Sphynx", "Dragon Li", "Dwelf", "Egyptian Mau",
    "European Shorthair", "Exotic Shorthair", "Foldex", "German Rex", "Havana Brown", "Highlander", "Himalayan", "Japanese Bobtail", "Javanese",
    "Karelian Bobtail", "Khao Manee", "Korat", "Korean Bobtail", "Korn Ja", "Kurilian Bobtai", "LaPerm", "Lykoi", "Maine Coon", "Manx", "Mekong Bobtail",
    "Minskin", "Munchkin", "Napoleon", "Nebelung", "Norwegian Forest Cat", "Ocicat", "Ojos Azules", "Oregon Rex", "Oriental Bicolor", "Oriental Longhair",
    "Oriental Shorthair", "Persian", "Peterbald", "Pixie-bob", "Raas", "Ragamuffin", "Ragdoll", "Russian Blue", "Russian White, Black, and Tabby",
    "Sam Sawet", "Savannah", "Scottish Fold", "Selkirk Rex", "Serengeti", "Serrade Petit", "Siamese", "Siberian", "Singapura", "Snowshoe", "Sokoke", "Somali",
    "Sphynx", "Suphalak", "Thai Lilac", "Tha", "Tonkinese", "Toyger", "Turkish Angora", "Turkish Van", "Ukrainian Levkoy", "Wila Krungthep", "York Chocolate"
]
SALE_COUNTRIES = ['China', 'USA', 'Europe']


class Robot:

    abilities = []

    def __new__(cls,  *args, **kwargs):
        cls.id = id(cls)
        cls.region = random.choice(SALE_COUNTRIES)
        return super().__new__(cls)

    @property
    def serial_number(cls):
        return '{}_{}'.format(cls.region.lower(), cls.id)

    @classmethod
    def save_ability(cls, cls_object, ability):
        if ability in cls.abilities:
            return False
        super(cls, cls_object).add_skill(ability)
        cls.abilities.append(ability)
        return True

    @classmethod
    def remove_ability(cls, cls_object, ability):
        if ability not in cls.abilities:
            return False
        super(cls, cls_object).forget_skill(ability)
        cls.abilities.remove(ability)
        return True

class Cat:

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.breed = random.choice(BREEDS)
        self.skills = []

    @property
    def knowledge_level(self):
        return len(self.skills)

    def add_skill(self, skill):
        if skill in self.skills:
            return False
        self.skills.append(skill)
        return True

    def forget_skill(self, skill):
        if skill not in self.skills:
            return False
        self.skills.remove(skill)
        return True


class RoboCat(Cat, Robot):

    def __init__(self, name, age):
        super().__init__(name, age)
        print(self.name, self.age, self.breed, self.serial_number)

    def add_skill(self, skill):
        print(skill)
        super().add_skill(skill)
        super().save_ability(self, skill)

    def remove_skill(self, skill):
        print(skill)
        super().forget_skill(skill)
        super().remove_ability(self, skill)

    def sync(self):
        "sync robot updates within all Robocats about known abilities (Robot variable can be used)"
        raise NotImplemented

    def sync(self):
        "sync robot updates within all Robocats about known abilities (gc or weakref)"
        raise NotImplemented


if __name__ == '__main__':

    skill = 'meow'
    
    rc = RoboCat("RoboCat", 20)

    rc.add_skill(skill)
    assert rc.abilities == [skill]
    assert rc.skills == [skill]

    rc.remove_skill(skill)
    assert rc.abilities == []
    assert rc.skills == []
