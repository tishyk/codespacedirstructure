import string


def task1(list1, list2):
    """
    Take two lists, say for example these two:

      a =[1,1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
      b =[1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    and write a program that returns a list that contains only the elements that are common between the lists (without duplicates).
    """
    return set(list1) & set(list2)


def task2(in_string):
    """
    Return the number of times that the letter “a” appears anywhere in the given string

    Given string is “I am a good developer. I am also a writer” and output should be 5.
    """
    return in_string.count("a")


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


def task10(in_string):
    """
    Write a program that will take the str parameter being passed and return the string in reversed order.
    For example: if the input string is "Hello World and Coders" then your program should return the string sredoC dna dlroW olleH.
    """
    return in_string[::-1]


def task11(number):
    """
    Write a program that will take the num parameter being passed and return the number of hours and minutes the parameter converts to (ie. if num = 63 then the output should be 1:3).
    Separate the number of hours and minutes with a colon.
    """
    return f"{number//60}:{number-60*(number//60)}"


def task12(in_string):
    """
    Write a program that will take the parameter being passed and return the largest word in the string.
    If there are two or more words that are the same length, return the first word from the string with that length.
    Ignore punctuation.

    Sample Test Cases:
    Input:"fun&!! time"
    Output:time
    Input:"I love dogs"
    Output:love
    """
    first_longest_word = None
    for word in in_string.split():
        word = "".join([symbol for symbol in word if symbol.isalpha()])
        if not first_longest_word or len(word) > len(first_longest_word):
            first_longest_word = word
    return first_longest_word

def task13(in_string):
    """
    Write a program (using functions!) that asks the user for a long string containing multiple words.
    Print back to the user the same string, except with the words in backwards order.

    For example:
    Input: My name is Michele
    Outout: Michele is name My
    """
    return " ".join(in_string.split()[::-1])

def task14(number):
    """
    Write a program that asks the user how many Fibonnaci numbers to generate and then generates them.
    Take this opportunity to think about how you can use functions.
    Make sure to ask the user to enter the number of numbers in the sequence to generate.
    (Hint: The Fibonnaci seqence is a sequence of numbers where the next number in the sequence is the sum of the previous two numbers in the sequence.
    The sequence looks like this: 1, 1, 2, 3, 5, 8, 13, …)
    """
    if number == 1:
        return [1]
    elif number == 2:
        return [1, 1]
    res_list = [1, 1]
    while len(res_list) != number:
        res_list.append(res_list[len(res_list)-2] + res_list[len(res_list)-1])
    return res_list


def task15(in_list):
    """
    Let’s say I give you a list saved in a variable: a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100].
    Write one line of Python that takes this list a and makes a new list that has only the even elements of this list in it.
    """
    return list(filter(lambda a: not a % 2, in_list))


def task16(number):
    """
    Write a program that will add up all the numbers from 1 to input number.
    For example: if the input is 4 then your program should return 10 because 1 + 2 + 3 + 4 = 10.
    """
    return sum(range(number + 1))


def task17(number):
    """
    Write a program that will take the parameter being passed and return the factorial of it.
    For example: if num = 4, then your program should return (4 * 3 * 2 * 1) = 24.
    """
    if number == 1:
        return 1
    return number * task17(number-1)


def task18(in_string):
    """
    Write a program that will take the str parameter being passed and modify it using the following algorithm.
    Replace every letter in the string with the letter following it in the alphabet (ie. c becomes d, z becomes a).
    Then capitalize every vowel in this new string (a, e, i, o, u) and finally return this modified string.

    Input: abcd
    Output: bcdE
    """
    letters = []
    for letter in in_string:
        if letter.islower():
            lower_letters = string.ascii_lowercase + "a"
            letter = lower_letters[lower_letters.index(letter) + 1]
        elif letter.isupper():
            upper_letters = string.ascii_uppercase + "A"
            letter = upper_letters[upper_letters.index(letter) + 1]
        if letter in ["a", "e", "i", "o", "u"]:
            letter = letter.upper()
        letters.append(letter)
    return "".join(letters)


def task19(in_string):
    """
    Write a program that will take the str string parameter being passed and return the string with the letters in alphabetical order (ie. hello becomes ehllo).
    Assume numbers and punctuation symbols will not be included in the string.

    Input: edcba
    Output: abcde
    """
    # return "".join([letter * in_string.count(letter) for letter in string.ascii_letters])
    return "".join(sorted(in_string))


def task20(num1, num2):
    """
    Write a program that will take both parameters being passed and return the true if num2 is greater than num1, otherwise return the false.
    If the parameter values are equal to each other then return the string -1
    """
    return True if num2 > num1 else False
