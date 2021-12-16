import sys
sys.path.append('../../../')

import argparse
from dataclasses import dataclass
from functools import reduce
import colorama


def part_one(in_file_name):
    in_file = open(in_file_name, 'r')


def part_two(in_file_name):
    in_file = open(in_file_name, 'r')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 12')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
