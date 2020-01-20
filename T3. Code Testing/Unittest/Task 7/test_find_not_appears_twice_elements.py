import unittest
from find_not_appears_twice_elements import find_not_appears_twice_elements


class TestFindNotAppearsTwiceElements(unittest.TestCase):
    def test_find_not_twice_els_1(self):
        self.assertEqual(find_not_appears_twice_elements([]), set())
        self.assertEqual(find_not_appears_twice_elements([2]), {2})

    def test_find_not_twice_els_2(self):
        self.assertEqual(find_not_appears_twice_elements([2, 3, 2]), {3})
        self.assertEqual(find_not_appears_twice_elements([5, 3, 4, 3, 4]), {5})
        self.assertEqual(find_not_appears_twice_elements([5, 3, 4, 3, 3]), {4, 5})

    def test_find_not_twice_els_3(self):
        with self.assertRaises(ValueError):
            find_not_appears_twice_elements(2)


if __name__ == "__main__":
    unittest.main()