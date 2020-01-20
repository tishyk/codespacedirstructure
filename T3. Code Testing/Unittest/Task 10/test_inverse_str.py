import unittest
from inverse_str import inverse_str


class TestInverseStr(unittest.TestCase):
    def test_inverse_str(self):
        self.assertEqual(inverse_str(""), "")
        self.assertEqual(inverse_str("a"), "a")

    def test_inverse_str_2(self):
        self.assertEqual(inverse_str("ab"), "ba")
        self.assertEqual(inverse_str("aba"), "aba")
        self.assertEqual(inverse_str("abbc"), "cbba")
        self.assertEqual(inverse_str("Hello World and Coders"), "sredoC dna dlroW olleH")

    def test_inverse_str_3(self):
        with self.assertRaises(ValueError):
            inverse_str(2)


if __name__  == "__main__":
    unittest.main()