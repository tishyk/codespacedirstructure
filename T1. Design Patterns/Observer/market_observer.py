from market_observer_interface import ObserverInterface, ObservableInterface


class Observable(ObservableInterface):
    def __init__(self):
        self.observers = []

    def register(self, observer):
        assert isinstance(observer, Observer), "Observer objects available to register only"
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def send_update(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def unregister_all(self):
        self.observers.clear()

class Observer(ObserverInterface):
    def __init__(self, name):
        self.name = name
        self.id = id(self)
        self.lead = False

    def update(self, *args, **kwargs):
        # do something on specific update
        self.lead = kwargs.get('lead', False)  #remove it to custom object

class AmericanMarket(Observer):
    def update(self, *args, **kwargs):
        print("American Market get next updates:{}; {}".format(args, kwargs))

class EuropeanMarket(Observer):
    def update(self, *args, **kwargs):
        print("European Market get next updates:{}; {}".format(args, kwargs))
