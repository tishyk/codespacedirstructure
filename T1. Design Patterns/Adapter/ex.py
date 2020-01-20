import json


def plot(data):
    pass


class GenXMLData():
    def get_xml(self):
        xml = True
        return xml


class Original():
    def render(self, data):
        if data:
            data = 1
        else:
            data = 0
        # data based logic
        return data * 10


class GenJsonData():
    def read_from_file(self, path):
        with open(path) as json_file:
            return json.load(json_file)


class Adapter(Original):
    precondition = ""

    def __init__(self, lib):
        self.lib = GenJsonData()

    def render(self, data):
        if isinstance(data, dict):
            if data.get("copyright"):
                data = 1
            else:
                data = 0
        if data:
            data = 1
        else:
            data = 0
        # data based logic
        return data * 10


x = Original().render()
x = Adapter().render()
plot(x)
