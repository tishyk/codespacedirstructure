def retry_decorator(func):

    def wrapper(*args, **kwargs):
        rc = 1
        for _ in range(3):
            rc = func(*args, **kwargs)
            if not rc:
                print("Success! \nReturned code: %d\n" % rc)
                break
        else:
            print("Error occurred. Please, try again. \nReturned code is: %d\n" % rc)
        return rc

    return wrapper
