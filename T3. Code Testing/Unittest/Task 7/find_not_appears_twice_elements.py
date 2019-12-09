def find_not_appears_twice_elements(elements):
    if type(elements) is not list:
        raise ValueError("Should be passed list")

    found_twice = set()
    found = set()
    for el in elements:
        if not el in found:
            found.add(el)
        else:
            found_twice.add(el)

    return set(elements) - found_twice