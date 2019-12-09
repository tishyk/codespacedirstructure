import string


def remove_punctuation(word):
    filtered = ""
    for ch in word:
        if ch in string.ascii_letters:
            filtered += ch

    return filtered


def find_largest_word(phrase):
    if type(phrase) is not str:
        raise ValueError("Value's type should be str")
    length = 0
    largest = ""
    for word in phrase.split():
        word = remove_punctuation(word)
        if len(word) > length:
            length = len(word)
            largest = word

    return largest