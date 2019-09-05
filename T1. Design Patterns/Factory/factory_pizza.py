import abc
class ABCPizzaFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_pizza(pizza_type):
        """ Do something
        # return Pizza object """
        pass

class Pizza(metaclass=abc.ABCMeta):
    def __init__(self):
        self._price = None

    @abc.abstractmethod
    def get_price(self):
        return self._price

class HamAndMushroomPizza(Pizza):
    def __init__(self):
        self._price = 8.5

    def get_price(self):
        return self._price

class DeluxePizza(Pizza):
    def __init__(self):
        self._price = 10.5

    def get_price(self):
        return self._price

class HawaiianPizza(Pizza):
    def __init__(self):
        self._price = 11.5

    def get_price(self):
        return self._price

class PizzaFactory(ABCPizzaFactory):
    def create_pizza(pizza_type):
        if pizza_type == 'HamMushroom':
            return HamAndMushroomPizza()
        elif pizza_type == 'Deluxe':
            return DeluxePizza()
        elif pizza_type == 'Hawaiian':
            return HawaiianPizza()
        else:
            raise AssertionError("Not implemented Pizza type")

if __name__ == '__main__':
    for pizza_type in ('HamMushroom', 'Deluxe', 'Hawaiian'):
          print('Price of {0} is {1}'.format(pizza_type, PizzaFactory.create_pizza(pizza_type).get_price()))
