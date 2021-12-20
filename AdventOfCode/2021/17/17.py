from io import FileIO
from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

INFINITY = 9223372036854775805

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


def part_one(in_file: FileIO, out_file: FileIO):
    target_spec = in_file.readline()
    target_spec = target_spec.strip().lstrip('target area: ')
    coords = [c.split('=') for c in target_spec.split(', ')]
    for coord in coords:
        coord[1] = coord[1].split('..')

    x_min = coords[0][1][0]
    x_max = coords[0][1][1]
    y_min = coords[1][1][0]
    y_max = coords[1][1][1]

    vxi = 1
    passed_x = False
    while not passed_x:


def main(file_name, part):
    with open(f'{file_name}.in', 'r', encoding='utf-8') as in_file:
        with open(f'{file_name}.{part}.out', 'w', encoding='utf-8') as out_file:
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
