import argparse

parser = argparse.ArgumentParser()
parser.add_argument('agent_ip', type=str, default='127.0.0.0', help="Agent IP address to obtaining the file system")
parser.add_argument('--ap', dest='password', type=str, help="Host 'root' password")
parser.add_argument('--master_ip', help=argparse.SUPPRESS)  # Argument transferred to ESD agent.py call

mgrp = parser.add_mutually_exclusive_group()
mgrp.add_argument('--xml', action='store_true', help="Get xml data")
mgrp.add_argument('--html', action='store_true', help="Get html data")
mgrp.add_argument('--yaml', action='store_true', help="Get yaml data")
mgrp.add_argument('--json', action='store_true', help="Get json data")

args = parser.parse_args()
print(args.agent_ip, args.agent_password)
print(args.master_ip)