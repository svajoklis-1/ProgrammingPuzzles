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

    x_min = int(coords[0][1][0])
    x_max = int(coords[0][1][1])
    y_min = int(coords[1][1][0])
    y_max = int(coords[1][1][1])

    print(x_min, x_max, y_min, y_max)

    highest_vyi = 0

    vyi = 0
    highest_y = 0
    done = False
    while not done:
        vy = vyi
        y = 0
        py = 0

        while y > y_min:
            y += vy
            if y > highest_y:
                highest_y = y
            vy -= 1

            if y < y_min:
                if py > y_max:
                    pass
                else:
                    highest_vyi = vyi
                    vyi += 1
                    print('New high', highest_vyi)
                    print('Highest y', highest_y)

                break

            py = y

        vyi += 1
        highest_y = 0

    print(highest_vyi)


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
