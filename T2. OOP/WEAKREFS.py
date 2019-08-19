from weakref import WeakMethod, WeakSet, WeakValueDictionary
import gc

class BigDataClass:
    def method(self):
        print("Hello")

bdc = BigDataClass()

wvd = WeakValueDictionary()
wvd['BDC'] = bdc
for k,v in wvd.items():
    print(k,v)

print(gc.get_threshold())
del bdc
gc.collect()

for k,v in wvd.items():
    print(k,v)