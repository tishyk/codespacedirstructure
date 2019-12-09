import unittest
from convert_minutes import convert_minutes


class TestConvertMinutes(unittest.TestCase):
    def test_convert_minutes(self):
        self.assertEqual(convert_minutes(0), "0:0")
        self.assertEqual(convert_minutes(45), "0:45")

    def test_convert_minutes_2(self):
        self.assertEqual(convert_minutes(63), "1:3")
        self.assertEqual(convert_minutes(60), "1:0")
        self.assertEqual(convert_minutes(1201), "20:1")

    def test_convert_minutes_3(self):
        with self.assertRaises(ValueError):
            convert_minutes("23")


if __name__ == "__main__":
    unittest.main()