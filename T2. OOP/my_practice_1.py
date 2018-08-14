class MyClass:

    def __init__(self, *args, **kwargs):
        args.x = 10
        kwargs.y = 'Hello'

    def print_x(self):
        print(args)

    def print_y(self):

        if not self.y:
            print('No y now')
        else:
            print(self.y)



c = MyClass(10)

c.print_x()
c.print_y()
print(c.y)
