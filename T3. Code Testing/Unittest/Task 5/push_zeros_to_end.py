def push_zeros_to_end(elements):
    if type(elements) is not list:
        raise ValueError("Should be passed object with type - list")
    zeros_count = elements.count(0)
    elements = [el for el in elements if el is not 0]
    for i in range(zeros_count):
        elements.append(0)

    return elements