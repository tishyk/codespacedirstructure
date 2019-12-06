import unittest
from fibonacci_sequence_generator import fibonacci_sequence_generate


class TestFibonnachiSequenceGenerate(unittest.TestCase):
    def test_fibonacci_sequence_generate(self):
        self.assertEqual(fibonacci_sequence_generate(0), [])
        self.assertEqual(fibonacci_sequence_generate(1), [0])
        self.assertEqual(fibonacci_sequence_generate(2), [0, 1])

    def test_fibonacci_sequence_generate_2(self):
        self.assertEqual(fibonacci_sequence_generate(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_fibonacci_sequence_generate_3(self):
        with self.assertRaises(ValueError):
            fibonacci_sequence_generate(-2)

        with self.assertRaises(ValueError):
            fibonacci_sequence_generate("smt")


if __name__ == "__main__":
    unittest.main()