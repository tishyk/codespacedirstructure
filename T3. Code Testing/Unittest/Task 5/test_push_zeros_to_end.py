import unittest
from push_zeros_to_end import push_zeros_to_end


class TestPushZerosToEnd(unittest.TestCase):
    def test_push_zeros_to_end_1(self):
        self.assertEqual(push_zeros_to_end(list()), list())
        self.assertEqual(push_zeros_to_end([0]), [0])
        self.assertEqual(push_zeros_to_end([1, 0]), [1, 0])

    def test_push_zeros_to_end_2(self):
        self.assertEqual(push_zeros_to_end([0, 1]), [1, 0])
        self.assertEqual(push_zeros_to_end([0, 1, 0]), [1, 0, 0])
        self.assertEqual(push_zeros_to_end([0, 2, 3, 4, 6, 7, 10]), [2, 3, 4, 6, 7, 10, 0])

    def test_push_zeros_to_end_3(self):
        self.assertEqual(push_zeros_to_end([0, "a", {"x": 10}]), ["a", {"x": 10}, 0])
        with self.assertRaises(ValueError):
            push_zeros_to_end(2)


if __name__ == "__main__":
    unittest.main()