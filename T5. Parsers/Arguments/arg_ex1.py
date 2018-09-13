import argparse

parser = argparse.ArgumentParser()
parser.add_argument('agent_ip', type=str, default='127.0.0.0', help="Agent IP address to obtaining the file system")
parser.add_argument('agent_password',metavar='password', type=str, help="Agent host 'root' password")
parser.add_argument('--master_ip', help=argparse.SUPPRESS)  # Argument transferred to ESD agent.py call

args = parser.parse_args()
print(args.agent_ip, args.agent_password)
print(args.master_ip)