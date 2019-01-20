# mc1 = MyClass("A")   --> MyClass obj
# mc2 = MyClass("A","B")        --> MyClass obj
# not_mc1 = MyClass("C")     --> object
# not_mc2 = MyClass("B","C")     --> object  #

class MyClass(object):

    def __init__(self, *args):
        if set(args).issubset(['A', 'B']):
            print("Create MyClass")
        if set(args).issubset(['B', 'C']):
            print("Create object")
            super().__init__() # TODO: Поки не зрозумів як створити базовий object замість кастомного

mc1 = MyClass("A")
mc2 = MyClass("A","B")
not_mc1 = MyClass("C")
not_mc2 = MyClass("B","C")
objects = [mc1, mc2, not_mc1, not_mc2, object()]
[print(type(x)) for x in objects]
