
class B:
    b = 10

class A:
    def __new__(cls, *args, **kwargs):
        self = super().__new__(B)
        return  self


    def __init__(self):
        pass

a = A()
