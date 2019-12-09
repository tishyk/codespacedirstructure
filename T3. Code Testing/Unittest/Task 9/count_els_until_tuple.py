def count_els_until_tuple(elements):
    if type(elements) is not list:
        raise ValueError("Should be passed list of elements")

    count = 0
    for el in elements:
        if type(el) is tuple:
            return count

        count += 1

    return count