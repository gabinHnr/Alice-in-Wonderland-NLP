import argparse
import requests

parser = argparse.ArgumentParser()
CalculType = parser.add_mutually_exclusive_group()
CalculType.add_argument('-a', '--add', action='store_true', help='Increase output verbosity.')
CalculType.add_argument('-s', '--sub', action='store_true', help='Increase output verbosity.')
CalculType.add_argument('-m', '--mul', action='store_true', help='Increase output verbosity.')
CalculType.add_argument('-d', '--div', action='store_true', help='Increase output verbosity.')

parser.add_argument("nbr1", help="nombre 1", type=int)
parser.add_argument("nbr2", help="nombre 2", type=int)

VariableType = parser.add_mutually_exclusive_group()
VariableType.add_argument('-f', '--float', action='store_true', help='Increase output verbosity.')
VariableType.add_argument('-i', '--int', action='store_true', help='Increase output verbosity.')

args = parser.parse_args()
if args.add:
    print (args.nbr1 + args.nbr2)
elif args.sub:
    print (args.nbr1 - args.nbr2)
elif args.mul:
    print(args.nbr1 * args.nbr2)
elif args.div:
    if args.int:
        print(args.nbr1 // args.nbr2)
    else:
        print(args.nbr1 / args.nbr2)