
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    @fullname.setter
    def fullname(self, name):
        self.first, self.last = name.split()
        return '{} {}'.format(self.first, self.last)


    @fullname.deleter
    def fullname(self):
        print("Delete name: {} {}".format(self.first, self.last))
        self.first, self.last = None, None


emp_1 = Employee('John', 'Smith')

print(emp_1.first)
print(emp_1.email)
print(emp_1.fullname)
emp_1.fullname = "Adam Smith"
print(emp_1.first)
print(emp_1.email)
print(emp_1.fullname)
del emp_1.fullname

