from weakref import WeakValueDictionary
import gc
class BigDataClass:
    def method(self):
        print("Hello")

bdc = BigDataClass()
wvd = WeakValueDictionary()
wvd[bdc] = "Hello"

for k, v in wvd.items():
    print(k, v)
    v.method()
    # v is available after for loop, one more link to object

del bdc
del v
gc.collect()
print(wvd['bookid'])
