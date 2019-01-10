class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last

    @property
    def fullname(self):
        print("Hello")
        return '{} {}'.format(self.first, self.last)

    @fullname.setter
    def fullname(self, last):
        self.last = last

    @fullname.deleter
    def fullname(self):
        print("Set None")
        self.first = None
        self.last = None

    @property
    def email(self):
        print("Hi")
        return '{}.{}@email.com'.format(self.first, self.last)


emp_1 = Employee('Corey', 'Schafer', 50000)
emp_2 = Employee('Test', 'Employee', 60000)

print(emp_1.fullname)
print(emp_2.email)
