from __future__ import print_function
import Pyro5.api


@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class Warehouse(object):
    def __init__(self):
        self.contents = ["chair", "bike", "flashlight", "laptop", "couch"]

    def list_contents(self):
        return self.contents

    def take(self, name, item):
        self.contents.remove(item)
        print("{0} took the {1}.".format(name, item))

    def store(self, name, item):
        self.contents.append(item)
        print("{0} stored the {1}.".format(name, item))


#  It will start a Pyro server for the warehouse object.
#  You can do this by registering your Pyro class with a ‘Pyro daemon’,
#  the server that listens for and processes incoming remote method calls.
def main():
    Pyro5.api.Daemon.serveSimple(
        {Warehouse: "example.warehouse"},
        ns=False, host="192.168.0.10", port=9000)


if __name__ == "__main__":
    main()
