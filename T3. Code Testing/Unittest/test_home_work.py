import HW1


def test_common_elements():
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    assert HW1.common_elements(a, b) == [1, 2, 3, 5, 8, 13]


def test_a_num():
    string = "I am a good developer. I am also a writer"
    assert HW1.a_num(string, 'a') == 5


def test_power_of_three():
    assert HW1.power_of_three(9)


def test_single_digit():
    assert HW1.single_digit(59) == 5


def test_zeros_to_the_end():
    f = [0, 2, 3, 0, 4, 6, 7, 0, 10]
    assert HW1.zeros_to_the_end(f) == [2, 3, 4, 6, 7, 10, 0, 0, 0]


def test_arithmetic_progression():
    assert HW1.arithmetic_progression([5, 7, 9, 11])


def test_single_num():
    assert HW1.single_num([5, 3, 4, 3, 4]) == 5


def test_find_missing():
    assert HW1.find_missing([1, 2, 3, 4, 6, 7, 8]) == 5


def test_count_elements():
    assert HW1.count_elements([1, 2, 3, (1, 2), 3]) == 3


def test_revert_string():
    string = 'Hello World and Coders'
    assert HW1.revert_string(string) == 'sredoC dna dlroW olleH'
