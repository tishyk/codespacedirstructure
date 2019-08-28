class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, seq):
        self.data = seq
        self.index = len(seq)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

rev = Reverse('spam')
next(rev)   # note no need to call iter()   #'m'
nums = Reverse(range(1,10))
next(nums)
