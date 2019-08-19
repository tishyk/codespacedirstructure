class MyClass():
    def __new__(cls, *args, **kwargs):
        if all((('A' in arg or 'B' in arg) for arg in args)):
            return super().__new__(cls)
        else:
            return object

    def __init__(*args, **kwargs):
        print("Object created")


mc1 = MyClass("A") #--> MyClass
mc2 = MyClass("A", "B") #--> MyClass
not_mc1 = MyClass("C") #--> object
not_mc2 = MyClass("B", "C") #--> object