import unittest
from count_a_appearing import count_a_appearing


class TestCountAAppearing(unittest.TestCase):
    def test_count_a_appearing_1(self):
        self.assertEqual(count_a_appearing(""), 0)
        self.assertEqual(count_a_appearing("a"), 1)
        self.assertEqual(count_a_appearing("aa"), 2)
        self.assertEqual(count_a_appearing("aaa"), 3)

    def test_count_a_appearing_2(self):
        self.assertEqual(count_a_appearing("b aB"), 1)
        self.assertEqual(count_a_appearing("c aaa"), 3)
        self.assertEqual(count_a_appearing("I am a good developer. I am also a writer"), 5)

    def test_count_a_appearing_3(self):
        self.assertEqual(count_a_appearing(["aaa"]), 0)


if __name__ == "__main__":
    unittest.main()