# This is an example of slot usage


class S:
    __slots__ = ['a', 'b', 'c']
    read = 10

x = S()
x.a = 10
x.var = 154444

"""
42
Traceback (most recent call last):
  File "slots_ex.py", line 12, in <module>
    x.new = "not possible"
AttributeError: 'S' object has no attribute 'new'
"""