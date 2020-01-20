import unittest
from find_missing_number import find_missing_number


class TestFindMissingNumber(unittest.TestCase):
    def test_find_missing_number(self):
        self.assertEqual(find_missing_number([1, 3]), 2)
        self.assertEqual(find_missing_number([1, 2, 4]), 3)

    def test_find_missing_number_2(self):
        self.assertEqual(find_missing_number([1, 2, 3, 4]), "Not found missing number")

    def test_find_missing_number_3(self):
        with self.assertRaises(ValueError):
            find_missing_number(3)

        with self.assertRaises(ValueError):
            find_missing_number([1, "3"])

        with self.assertRaises(ValueError):
            find_missing_number([])

        with self.assertRaises(ValueError):
            find_missing_number([1])


if __name__ == "__main__":
    unittest.main()