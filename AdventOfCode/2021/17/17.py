from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

INFINITY = 9223372036854775805

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


def part_one(in_file, out_file):


def main(in_file, part):
    with open(f'{in_file}.in', 'r', encoding='utf-8') as in_file:
        with open(f'{in_file}.{part}.out', 'w', encoding='utf-8') as out_file:
            match part:
                case 'one':
                    part_one(in_file, out_file)
                case 'two':
                    part_two(in_file, out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 16')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    main(args.in_file, args.part)
