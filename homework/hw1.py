class MyClass:
    def __new__(cls, *args):
        if set(args).issubset({"A", "B"}):
            return super().__new__(cls)
        else:
            return object

    def __init__(*args):
        pass


if __name__ == '__main__':
    mc1 = MyClass("A")
    mc2 = MyClass("A", "B")
    not_mc1 = MyClass("C")
    not_mc2 = MyClass("B", "C")

    print(mc1, mc2, not_mc1, not_mc2, sep="\n")
