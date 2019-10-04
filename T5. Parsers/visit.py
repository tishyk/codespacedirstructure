#!/usr/bin/python3

# This is the code that runs this example.
import Pyro5.api
import argparse
from person import Person

parser = argparse.ArgumentParser()


parser.add_argument('uri', type=str, metavar="URI", default='PYRO:argument.warehouse@192.168.0.10:9000',
                    help="URI address to obtaining the pyro server")

parser.add_argument('-d', '--deposit', type=str, default='laptop', help="Item to store")
parser.add_argument('-r', '--retrive', type=str, default='laptop', help="Item to take")

mgrp = parser.add_mutually_exclusive_group()
mgrp.add_argument('--xml', action='store_true', help="Set xml data")
mgrp.add_argument('--yaml', action='store_true', help="Set yaml data")
mgrp.add_argument('--json', action='store_true', help="Set json data")

args = parser.parse_args()

warehouse = Pyro5.api.Proxy(args.uri)
janet = Person("Janet")

#janet.visit(warehouse, retrive=args.retrive, deposit=args.deposit)
#janet.create_xml()
#janet.create_json(True)
janet.send_data(warehouse, args)