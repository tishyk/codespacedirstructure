import unittest
import homework


class MyTestCase(unittest.TestCase):
    def test_task1(self):
        a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.assertEqual({1, 2, 3, 5, 8, 13}, set(homework.task1(a, b)))

    def test_task2(self):
        test_string = "I am a good developer. I am also a writer"
        self.assertEqual(5, homework.task2(test_string))

    def test_task3(self):
        num = 9
        self.assertEqual(True, homework.task3(num))
        self.assertTrue(homework.task3(num))
        num = 8
        self.assertFalse(homework.task3(num))

    def test_task4(self):
        num = 59
        self.assertEqual(5, homework.task4(num))
        num = 134
        self.assertEqual(8, homework.task4(num))

    def test_task5(self):
        test_list = [0, 2, 3, 4, 6, 7, 10]
        self.assertEqual([2, 3, 4, 6, 7, 10, 0], homework.task5(test_list))
        test_list = [0, 2, 3, 4, 0, 0, 6, 7, 10]
        self.assertEqual([2, 3, 4, 6, 7, 10, 0, 0, 0], homework.task5(test_list))
        test_list = [2, 3, 4, 6, 7, 10]
        self.assertEqual([2, 3, 4, 6, 7, 10], homework.task5(test_list))

    def test_task6_1(self):
        test_list = [5, 7, 9, 11]
        self.assertTrue(homework.task6_1(test_list))
        test_list = [5, 7, 9, 111]
        self.assertFalse(homework.task6_1(test_list))

    def test_task6_2(self):
        test_list = [5, 7, 9, 11]
        self.assertTrue(homework.task6_2(test_list))
        test_list = [5, 7, 9, 111]
        self.assertFalse(homework.task6_2(test_list))

    def test_task7(self):
        test_list = [5, 3, 4, 3, 4]
        self.assertEqual(5, homework.task7(test_list))
        test_list = [5, 3, 4, 3, 4, 5]
        self.assertIsNone(homework.task7(test_list))
        test_list = [1, 2]
        self.assertEqual(1, homework.task7(test_list))

    def test_task8(self):
        test_list = [1, 2, 3, 4, 6, 7, 8]
        self.assertEqual(5, homework.task8(test_list))
        test_list = [6, 7, 8, 10, 11]
        self.assertEqual(9, homework.task8(test_list))
        test_list = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertIsNone(homework.task8(test_list))
        test_list = [-3, -2, -1, 1]
        self.assertEqual(0, homework.task8(test_list))

    def test_task9(self):
        test_list = [1, 2, 3, (1, 2), 3]
        self.assertEqual([1, 2, 3], homework.task9(test_list))

    def test_task10(self):
        test_string = "Hello World and Coders"
        self.assertEqual("sredoC dna dlroW olleH", homework.task10(test_string))

    def test_task11(self):
        num = 63
        self.assertEqual("1:3", homework.task11(num))
        num = 15
        self.assertEqual("0:15", homework.task11(num))
        num = 179
        self.assertEqual("2:59", homework.task11(num))

    def test_task12(self):
        test_string = "fun&!! time"
        self.assertEqual("time", homework.task12(test_string))
        test_string = "I love dogs"
        self.assertEqual("love", homework.task12(test_string))

    def test_task13(self):
        test_string = "My name is Michele"
        self.assertEqual("Michele is name My", homework.task13(test_string))

    def test_task14(self):
        num = 1
        self.assertEqual([1], homework.task14(num))
        num = 2
        self.assertEqual([1, 1], homework.task14(num))
        num = 7
        self.assertEqual([1, 1, 2, 3, 5, 8, 13], homework.task14(num))

    def test_task15(self):
        test_list = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        self.assertEqual([4, 16, 36, 64, 100], homework.task15(test_list))

    def test_task16(self):
        num = 4
        self.assertEqual(10, homework.task16(num))

    def test_task17(self):
        num = 4
        self.assertEqual(24, homework.task17(num))

    def test_task18(self):
        test_string = "abcd"
        self.assertEqual("bcdE", homework.task18(test_string))
        test_string = "bazaar"
        self.assertEqual("cbAbbs", homework.task18(test_string))

    def test_task19(self):
        test_string = "hello"
        self.assertEqual("ehllo", homework.task19(test_string))
        test_string = "edCBa"
        self.assertEqual("BCade", homework.task19(test_string))

    def test_task20(self):
        num1 = num2 = 2
        self.assertFalse(homework.task20(num1, num2))
        num2 = 3
        self.assertTrue(homework.task20(num1, num2))
        num2 = 1
        self.assertFalse(homework.task20(num1, num2))


if __name__ == '__main__':
    unittest.main()
