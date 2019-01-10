def gen(i):
    var = 10
    I = iter(i)
    yield next(I)

for x in gen((1,2,3)):
    print(x)
