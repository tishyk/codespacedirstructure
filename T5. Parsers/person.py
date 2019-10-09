import os
import xml.etree.ElementTree as ET
import json
import base64
import yaml


class Person(object):
    def __init__(self, name):
        self.name = name

    def visit(self, warehouse, retrive, deposit=''):
        print("This is {0}.".format(self.name))
        self.retrieve(warehouse, retrive)
        self.deposit(warehouse, deposit)
        print("Thank you, come again!")

    def deposit(self, warehouse, item=None):
        print("The warehouse contains:", warehouse.list_contents())
        if item is None:
            item = input("Type a thing you want to store: ").strip()
        if item:
            print(f"You store {item}")
            warehouse.store(self.name, item)

    def retrieve(self, warehouse, item=None):
        print("The warehouse contains:", warehouse.list_contents())
        if item is None:
            item = input("Type something you want to take (or empty): ").strip()
        if item:
            print(f"You take {item}")
            warehouse.take(self.name, item)

    def send_data(self, warehouse, datatypes, data=""):
        if datatypes.xml:
            datatype = 'xml'
            data = self.create_xml()
        elif datatypes.json:
            datatype = 'json'
            data = self.create_json(to_file=True)
        elif datatypes.yaml:
            datatype = 'yaml'
        else:
            raise RuntimeError("Incorrect datatype")
        print(f"Send to warehouse server datatype {datatype}")
        warehouse.transfer(self.name, datatype, data)

    def create_xml(self, to_file=None):
        env = os.environ

        # create the file structure
        root = ET.Element(env['USERNAME'])
        os_items = ET.SubElement(root, 'system')
        for key in env.keys():
            if 'OS' in key or 'PROCESSOR' in key or 'LC' in key:
                system_item = ET.SubElement(os_items, 'system_attribute')
                system_item.set('name', key)
                system_item.text = env[key]

        mydata = ET.tostringlist(root, encoding="unicode", method='xml')
        if to_file:
            # create a new XML file with the results
            with open("computer.xml", "w") as xml_file:
                xml_file.writelines(mydata)

        return mydata

    def create_json(self, to_file=None):
        env = dict(os.environ)
        json_string = json.dumps(env)
        if to_file:
            # create a new XML file with the results
            with open("computer.json", "w") as json_file:
                json.dump(env, json_file, indent=3)
        return json_string
