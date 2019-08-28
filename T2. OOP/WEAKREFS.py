from weakref import WeakValueDictionary
import gc


class BigDataClass:
    def method(self):
        print("Hello")


bdc = BigDataClass()

wvd = WeakValueDictionary()

wvd['bookid'] = bdc

for k, v in wvd.items():
    print(k, v)
    # v is available after for loop, one more link to object

del bdc
del v
gc.collect()

print(wvd['bookid'])
