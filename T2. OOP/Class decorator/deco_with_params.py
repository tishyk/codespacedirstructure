def decorators(*args, **kwargs):
    def inner(function):
        '''
        do operations with func
        '''

        print(kwargs.get('dkey'))
        return function
    return inner  # this is the fun_obj mentioned in the above content


@decorators(dkey='value')
def func(x):
    print("inside function", x)

func(10)
