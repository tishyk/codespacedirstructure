import unittest
from lists_common_elements import get_common_elements


class TestGetCommonElements(unittest.TestCase):
    def test_getCommonElements_1(self):
        #  All passed easy for first variant of get_common_elements
        self.assertEqual(get_common_elements([1], [1]), [1])
        self.assertEqual(get_common_elements([1, 2], [1]), [1])
        self.assertEqual(get_common_elements([1, 2, 3], [2, 3, 4]), [2, 3])
        self.assertEqual(get_common_elements(["a", "b"], ["b"]), ["b"])

    def test_getCommonElements_2(self):
        self.assertEqual(get_common_elements([1, 2], [3, 4]), list())
        self.assertEqual(get_common_elements(["2", "3"], ["3", "4"]), ["3"])
        # List is not hashable type - solution should be improved
        self.assertEqual(get_common_elements([["a", "b"], ["b", "c"]], [["a", "c"], ["b", "c"]]), [["b", "c"]])

    def test_getCommonElements_3(self):
        self.assertEqual(get_common_elements([1, "23", ["345"]], [{"x": 10}, (2, 3, 8)]), list())
        self.assertEqual(get_common_elements([1, "23", ["345"], {"x": 10, "z": 20}], [{"x": 10}, (2, 3, 8), ["345"]]), [["345"]])
        self.assertEqual(get_common_elements([1, "23", {"x": 10}], [{"x": 10}, 2]), [{"x": 10}])
        self.assertEqual(get_common_elements([(1, 2), (2, 3, 4)], [(2, 3, 4), "238"]), [(2, 3, 4)])


if __name__ == "__main__":
    unittest.main()