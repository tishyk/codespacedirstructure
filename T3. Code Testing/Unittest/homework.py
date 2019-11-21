def task1(list1, list2):
    """
    Take two lists, say for example these two:

      a =[1,1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
      b =[1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    and write a program that returns a list that contains only the elements that are common between the lists (without duplicates).
    """
    return set(list1) & set(list2)


def task2(string):
    """
    Return the number of times that the letter “a” appears anywhere in the given string

    Given string is “I am a good developer. I am also a writer” and output should be 5.
    """
    return string.count("a")


def task3(number):
    """
    Write a Python program to check if a given positive integer is a power of three

    Input : 9
    Output : True
    """
    return not number % 3


def task4(number):
    """
    Write a Python program to add the digits of a positive integer repeatedly until the result has a single digit.

    Input : 48
    Output : 3

    For example given number is 59, the result will be 5.
    Step 1: 5 + 9 = 14
    Step 1: 1 + 4 = 5
    """
    while number > 10:
        number = sum(list(map(int, list(str(number)))))
    return number


def task5(in_list):
    """
    Write a Python program to push all zeros to the end of a list.

    Input : [0,2,3,4,6,7,10]
    Output : [2, 3, 4, 6, 7, 10, 0]
    """
    return [x for x in in_list if x != 0] + [0] * in_list.count(0)


def task6_1(in_list):
    """
    Write a Python program to check a sequence of numbers is an arithmetic progression or not.

    Input : [5, 7, 9, 11]
    Output : True

    In mathematics, an arithmetic progression or arithmetic sequence is a sequence of numbers such that the difference between the consecutive terms is constant.
    For example, the sequence 5, 7, 9, 11, 13, 15 ... is an arithmetic progression with common difference of 2.
    """
    if len(in_list) <= 2:
        return True
    diff = in_list[1] - in_list[0]
    elem_prev = in_list[1]
    for elem in in_list[2:]:
        if elem - elem_prev != diff:
            return False
        elem_prev = elem
    return True


def task6_2(in_list):
    """See task6_1."""
    diff_list = [x - in_list[i-1] for i, x in enumerate(in_list) if i != 0]
    return len(set(diff_list)) == 1


def task7(in_list):
    """
    Write a Python program to find the number in a list that doesn't occur twice.

    Input : [5, 3, 4, 3, 4]
    Output : 5
    """
    temp_list = in_list.copy()
    for i in range(len(temp_list)):
        if not temp_list:
            return None
        if temp_list.count(temp_list[0]) == 1:
            return temp_list[0]
        temp_list = list(filter(lambda a: a != temp_list[0], temp_list))
    return None


def task8(in_list):
    """
    Write a Python program to find a missing number from a list.

    Input : [1,2,3,4,6,7,8]
    Output : 5
    """
    missing = sum([x for x in range(min(in_list), max(in_list)+1)]) - sum(in_list)
    if missing == 0:
        if (1 in in_list) and (-1 in in_list) and (0 not in in_list):
            missing = 0
        else:
            missing = None
    return missing


def task9(in_list):
    """
    Write a Python program to count the elements in a list until an element is a tuple.

    Sample Test Cases:
    Input: [1,2,3,(1,2),3]
    Output: 3
    """
    res_list = []
    for elem in in_list:
        if isinstance(elem, tuple):
            break
        res_list.append(elem)
    return res_list


def task10(string):
    """
    Write a program that will take the str parameter being passed and return the string in reversed order.
    For example: if the input string is "Hello World and Coders" then your program should return the string sredoC dna dlroW olleH.
    """
    return string[::-1]
