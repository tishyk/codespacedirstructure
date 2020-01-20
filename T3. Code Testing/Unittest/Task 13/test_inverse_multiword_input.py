import unittest
from inverse_multiword_input import inverse_multiword_input


def input_getter_1():
    return "Something"


def input_getter_2():
    return "My name is Michele"


class TestInverseMultiwordInput(unittest.TestCase):
    def test_inverse_multiword_input(self):
        self.assertEqual(inverse_multiword_input(input_getter_1), "Something")

    def test_inverse_multiword_input_2(self):
        self.assertEqual(inverse_multiword_input(input_getter_2), "Michele is name My")


if __name__ == "__main__":
    unittest.main()