import argparse

"""
name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
action - The basic type of action to be taken when this argument is encountered at the command line.
nargs - The number of command-line arguments that should be consumed.
const - A constant value required by some action and nargs selections.
default - The value produced if the argument is absent from the command line.
type - The type to which the command-line argument should be converted.
choices - A container of the allowable values for the argument.
required - Whether or not the command-line option may be omitted (optionals only).
help - A brief description of what the argument does.
metavar - A name for the argument in usage messages.
dest - The name of the attribute to be added to the object returned by parse_args().
"""

parser = argparse.ArgumentParser()
parser.add_argument('agent_ip', type=str, default='127.0.0.0', help="Agent IP address to obtaining the file system")
parser.add_argument('agent_password',metavar='password', type=str, help="Agent host 'root' password")
parser.add_argument('--master_ip', help=argparse.SUPPRESS)  # Argument transferred to ESD agent.py call

args = parser.parse_args()
print(args.agent_ip, args.agent_password)
print(args.master_ip)
