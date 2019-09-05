"""
Specify the kinds of objects to create using a prototypical instance,
and create new objects by copying this prototype.
"""

import copy


class Prototype:
    """
    Example class to be copied.
    """
    pass
    def clone(self):
        return copy.deepcopy(self)


def main():
    prototype = Prototype()
    prototype_copy = prototype.clone()


if __name__ == "__main__":
    main()