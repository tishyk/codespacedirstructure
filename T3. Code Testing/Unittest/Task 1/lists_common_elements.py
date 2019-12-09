UNHASHABLE_TYPES = [list, dict]


def consists_unhashable_type(elements):
    for el in elements:
        if type(el) in UNHASHABLE_TYPES:
            return True

    return False


def get_common_elements_by_convertion_to_set(first, second):
    return list(set(first) & set(second))


def get_common_elements_one_by_one(first, second):
    common = []
    for el1 in first:
        for el2 in second:
            if el1 == el2:
                common.append(el1)

    return common


def get_common_elements(first, second):
    if consists_unhashable_type(first) or consists_unhashable_type(second):
        return get_common_elements_one_by_one(first, second)

    return get_common_elements_by_convertion_to_set(first, second)