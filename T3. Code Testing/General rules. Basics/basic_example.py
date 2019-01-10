import itertools

def rle(iterable):
    """
    Applies run-length encoding to an iterable.
    """
    for item, g in itertools.groupby(iterable):
        yield item, sum((1 for _ in g))

def test_rle():
    print(list(rle("mississippi")))

test_rle()
