class Connection:
    def __getattribute__(self, item):
        if item == "ip":
            self.ip = "10.151.66.10"
        return super().__getattribute__(item)

    def __getattr__(self, item):
        print(item)

    def __setattr__(self, key, value):
        if key == "host_ip":
            assert isinstance(value, str), "Not string"
        self.__class__.__dict__[key] = value

c = Connection()
c.ip
c.host = "win"
c.host_ip = "hello"
print(c.host_ip)
