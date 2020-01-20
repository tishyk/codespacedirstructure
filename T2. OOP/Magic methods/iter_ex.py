class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, seq):
        self.data = seq
        self.index = len(seq)

    def __iter__(self):
        return self

    def __next__(self):
        self.index = self.index - 1
        try:
            result = self.data[self.index]
        except IndexError:
            raise StopIteration
        return result

rev = Reverse('spam')
for i in rev:
    print(i)   # note no need to call iter()   #'m'
nums = Reverse(range(1,10))
(next(nums))
