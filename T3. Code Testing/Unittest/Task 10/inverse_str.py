def inverse_str(string):
    if type(string) is not str:
        raise ValueError("Should be passed str as input")

    return string[::-1]