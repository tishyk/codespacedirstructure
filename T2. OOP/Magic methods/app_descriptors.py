# Application Descriptors

class IP_Descriptor():
    def __init__(self, name):
        self.ip_variable_name = name

    def __get__(self, instance, cls):
        # instance: is the instance being manipulated
        # e.q. SSH instance
        print(f"IP variable used:{self.ip_variable_name}")
        print("IP address used:{}".format(instance.__dict__[self.ip_variable_name]))
        return instance.__dict__[self.ip_variable_name]

    def __set__(self, instance, value):
        if instance.connected:
            raise RuntimeError("Could not set ip address for existed connection")
        else:
            instance.__dict__[self.ip_variable_name] = value

    def __delete__(self, instance):
        print("Delete:", self.ip_variable_name)
        del instance.__dict__[self.ip_variable_name]
