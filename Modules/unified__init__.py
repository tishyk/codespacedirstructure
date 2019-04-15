# spam/
#   |
#   - foo.py   ---> class Foo ...
#   - bar.py   ---> class Bar ...
#   - __init__.py ---> from .foo import Foo
#                      from .bar import Bar

import spam
f = spam.Foo()
b  = spam.Bar()
