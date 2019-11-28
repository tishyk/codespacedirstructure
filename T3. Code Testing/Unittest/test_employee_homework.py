import unittest
from employee import Employee


class TestEmployee(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.e_1 = Employee("Quentin", "Tarantino", 2300)
        cls.e_2 = Employee("Pavlo", "Zibrov", 1050)

    def test_inst_attr(self):
        self.assertEqual("Quentin", self.e_1.first)
        self.assertEqual("Tarantino", self.e_1.last)
        self.assertEqual(2300, self.e_1.pay)
        self.assertEqual("Pavlo", self.e_2.first)
        self.assertEqual("Zibrov", self.e_2.last)
        self.assertEqual(1050, self.e_2.pay)

    def test_email(self):
        self.assertEqual("Quentin.Tarantino@email.com", self.e_1.email)
        self.assertEqual("Pavlo.Zibrov@email.com", self.e_2.email)

        self.e_1.first = "Pavlo"
        self.e_2.last = "Timberlake"
        self.assertEqual("Pavlo.Tarantino@email.com", self.e_1.email)
        self.assertEqual("Pavlo.Timberlake@email.com", self.e_2.email)

    def test_fullname(self):
        self.assertEqual("Quentin Tarantino", self.e_1.fullname)
        self.assertEqual("Pavlo Zibrov", self.e_2.fullname)

        self.e_1.last = "Zibrov"
        self.e_2.first = "John"
        self.assertEqual("Quentin Zibrov", self.e_1.fullname)
        self.assertEqual("John Zibrov", self.e_2.fullname)

    def test_apply_raise(self):
        self.e_1.apply_raise()
        self.assertEqual(2415, self.e_1.pay)
        self.e_1.apply_raise()
        self.assertEqual(2535, self.e_1.pay)
        self.e_2.apply_raise()
        self.assertEqual(1102, self.e_2.pay)


if __name__ == '__main__':
    unittest.main()
