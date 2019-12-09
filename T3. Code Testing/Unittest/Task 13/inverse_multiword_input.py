def ask_phrase():
    return input("Please write some phrase: \n")


def inverse_multiword_input(input_getter=ask_phrase):
    user_phrase = input_getter()
    if len(user_phrase.split()) < 2:
        return user_phrase

    return " ".join(user_phrase.split()[::-1])