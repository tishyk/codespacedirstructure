import unittest
from convert_number_to_digit import convert_number_to_digit


class TestConvertNumberToDigit(unittest.TestCase):
    def test_convert_number_to_digit_1(self):
        self.assertEqual(convert_number_to_digit(0), 0)
        self.assertEqual(convert_number_to_digit(1), 1)
        self.assertEqual(convert_number_to_digit(7), 7)

    def test_convert_number_to_digit_2(self):
        self.assertEqual(convert_number_to_digit(11), 2)
        self.assertEqual(convert_number_to_digit(23), 5)
        self.assertEqual(convert_number_to_digit(48), 3)

    def test_convert_number_to_digit_3(self):
        with self.assertRaises(ValueError):
            convert_number_to_digit(3.8)

        with self.assertRaises(ValueError):
            convert_number_to_digit(-2)


if __name__ == "__main__":
    unittest.main()