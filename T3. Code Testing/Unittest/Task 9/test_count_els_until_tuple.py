import unittest
from count_els_until_tuple import count_els_until_tuple


class TestCountElsUntilTuple(unittest.TestCase):
    def test_count_els_until_tuple(self):
        self.assertEqual(count_els_until_tuple([]), 0)
        self.assertEqual(count_els_until_tuple([1]), 1)
        self.assertEqual(count_els_until_tuple([1, 2, 3]), 3)

    def test_count_els_until_tuple_2(self):
        self.assertEqual(count_els_until_tuple([(1, 2)]), 0)
        self.assertEqual(count_els_until_tuple([(1, 2), 1]), 0)
        self.assertEqual(count_els_until_tuple([1, 2, (1, 2)]), 2)
        self.assertEqual(count_els_until_tuple([1, 2, (1, 2), 3]), 2)

    def test_count_els_until_tuple_3(self):
        with self.assertRaises(ValueError):
            count_els_until_tuple(2)


if __name__ == "__main__":
    unittest.main()