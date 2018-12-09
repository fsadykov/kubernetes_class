#!/usr/bin/python3
import data
import time
import argparse

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag' )


parser.add_argument('--test',action='store_true')
args = parser.parse_args()

if args.verbose:
    print("~ Verbose!")
elif args.test:
    print('~ Test!')
else:
    print("~ Not so verbose")
