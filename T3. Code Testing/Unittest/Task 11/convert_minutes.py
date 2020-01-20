def convert_minutes(minutes):
    if type(minutes) is not int:
        raise ValueError("Should be passed int value")

    return "{}:{}".format(int(minutes / 60), minutes - 60 * int(minutes / 60))