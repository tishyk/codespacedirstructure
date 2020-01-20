import unittest
from find_largest_word import find_largest_word


class TestFindLargestWord(unittest.TestCase):
    def test_find_largest_word(self):
        self.assertEqual(find_largest_word(""), "")
        self.assertEqual(find_largest_word("one"), "one")

    def test_find_largest_word_2(self):
        self.assertEqual(find_largest_word("one two three"), "three")
        self.assertEqual(find_largest_word("two one"), "two")
        self.assertEqual(find_largest_word("I love dogs"), "love")

    def test_find_largest_word_3(self):
        self.assertEqual(find_largest_word("!two one"), "two")

    def test_find_largest_word_4(self):
        with self.assertRaises(ValueError):
            raise find_largest_word(2)


if __name__ == "__main__":
    unittest.main()