import argparse
"""
ArgumentParser.add_argument(
    name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
    
Define how a single command-line argument should be parsed.
Each parameter has its own more detailed description below, but in short they are:

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

# an optional argument could be created like:
parser.add_argument('-m', '--master_ip')


# while a positional argument could be created like
parser.add_argument('ip')


#'store' - This just stores the argument’s value.  This is the default action. For example:
#parser.add_argument('--retry')
#parser.parse_args('--retry 1'.split())

parser.add_argument('--retry', action='store_const', const=5)


# 'store_true' and 'store_false' - These are special cases of 'store_const' used for storing
# the values True and False respectively. In addition, they create default values of False and True respectively.
# For example:

parser.add_argument('--wait_connection', action='store_true')
parser.add_argument('--retry_on_fail', action='store_false')

#'append_const' - This stores a list, and appends the value specified by the const keyword argument to the list.
# The 'append_const' action is typically useful when multiple arguments need to store constants to the same list.
# For example:
parser.add_argument('--str', dest='types', action='append_const', const=str)
parser.add_argument('--int', dest='types', action='append_const', const=int)
parser.parse_args('--str --int'.split())
# ---> Namespace(types=[<class 'str'>, <class 'int'>])


# 'count' - This counts the number of times a keyword argument occurs.
# For example, this is useful for increasing verbosity levels

parser.add_argument('--verbose', '-v', action='count')
parser.parse_args(['-vvv'])
# ---> Namespace(verbose=3)


# 'version' - This expects a version= keyword argument in the add_argument() call,
# and prints version information and exits when invoked:
parser = argparse.ArgumentParser(prog='Code Space')
parser.add_argument('--version', action='version', version='%(prog)s 2.0')
parser.parse_args(['--version'])
# ---> Code Space 2.0

args = parser.parse_args()
print(args.agent_ip, args.agent_password)
print(args.master_ip)