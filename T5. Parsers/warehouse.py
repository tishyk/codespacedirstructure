import Pyro5.api
import xml.etree.ElementTree as ET
import json
import base64

@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class Warehouse(object):
    def __init__(self):
        self.data = None
        self.contents = ["chair", "bike", "flashlight", "laptop", "couch"]

    def list_contents(self):
        return self.contents

    def take(self, name, item):
        self.contents.remove(item)
        print("{0} took the {1}.".format(name, item))

    def store(self, name, item):
        self.contents.append(item)
        print("{0} stored the {1}.".format(name, item))

    def transfer(self, name, datatype, data):
        print(f"{name} just send to the server {datatype} data type")
        if datatype == 'xml':
            with open(f"computer_{name}.xml", "w") as xml_file:
                xml_file.writelines(data)
        if datatype == 'json':
            data_dict = json.loads(data)
            with open(f"computers.json", 'rb') as json_file:
                common_data = json.load(json_file)
                common_data.update(data_dict)
            with open(f"computers.json", "w", ) as json_file:
                json.dump(common_data, json_file, indent=3)

#  It will start a Pyro server for the warehouse object.
#  You can do this by registering your Pyro class with a ‘Pyro daemon’,
#  the server that listens for and processes incoming remote method calls.
def main():
    Pyro5.api.Daemon.serveSimple(
        {
            Warehouse: "argument.warehouse"
        },
        ns=False, host="192.168.0.10", port=9000)


if __name__ == "__main__":
    main()
