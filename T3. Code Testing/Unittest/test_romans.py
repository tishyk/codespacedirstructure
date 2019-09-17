import unittest
from romans import sum


class TestRomans(unittest.TestCase):
    def test_I(self):
        self.assertEqual(sum("I", "I"), "II")
        self.assertEqual(sum("I", "II"), "III")
        self.assertEqual(sum("II", "II"), "IIII")

    def test_V(self):
        self.assertEqual(sum("I", "IIII"), "V")
        self.assertEqual(sum("II", "III"), "V")

    def test_VI(self):
        self.assertEqual(sum("II", "IIII"), "VI")
        self.assertEqual(sum("III", "III"), "VI")
        self.assertEqual(sum("V", "I"), "VI")

    def test_VII(self):
        self.assertEqual(sum("V", "II"), "VII")
        self.assertEqual(sum("VI", "I"), "VII")
        self.assertEqual(sum("III", "IIII"), "VII")

    def test_VIII(self):
        self.assertEqual(sum("V", "III"), "VIII")
        self.assertEqual(sum("IIII", "IIII"), "VIII")
        self.assertEqual(sum("III", "V"), "VIII")

    def test_X(self):
        self.assertEqual(sum("V", "V"), "X")
        self.assertEqual(sum("VI", "IIII"), "X")
        self.assertEqual(sum("VII", "III"), "X")
        self.assertEqual(sum("II", "VIII"), "X")

    def test_VIIII(self):
        self.assertEqual(sum("V", "IIII"), "VIIII")
        self.assertEqual(sum("VI", "III"), "VIIII")
        self.assertEqual(sum("VIII", "I"), "VIIII")

    def test_L(self):
        self.assertEqual(sum("XX", "XXX"), "L")
        self.assertEqual(sum("XXVI", "XXIIII"), "L")


if __name__ == '__main__':
    unittest.main()
