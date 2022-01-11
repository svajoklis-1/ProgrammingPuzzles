from io import FileIO
from os import stat
import sys
import argparse
from math import floor, ceil, sqrt

from dataclasses import dataclass
from functools import reduce
from enum import Enum, auto

import re

INFINITY = 9223372036854775805

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


class Vec2:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def clone(self) -> 'Vec2':
        return Vec2(self.x, self.y)

    def remap(self, remap: str) -> 'Vec2':
        new_vec = self.clone()

        match remap[1]:
            case 'x':
                new_vec.x = self.x
            case 'y':
                new_vec.x = self.y

        match remap[0]:
            case '-':
                new_vec.x = -new_vec.x

        match remap[3]:
            case 'x':
                new_vec.y = self.x
            case 'y':
                new_vec.y = self.y

        match remap[2]:
            case '-':
                new_vec.y = -new_vec.y

        return new_vec

    def subtract(self, other: 'Vec2'):
        return Vec2(self.x - other.x, self.y - other.y)

    def add(self, other: 'Vec2'):
        return Vec2(self.x + other.x, self.y + other.y)

    def equal(self, other: 'Vec2'):
        return self.x == other.x and self.y == other.y

    def distance_to(self, other):
        return sqrt(pow(self.x - other.x, 2), pow(self.y - other.y))


class Vec2Map:
    vectors: list[Vec2]

    def __init__(self):
        self.vectors = []

    def append(self, vec: Vec2):
        self.vectors.append(vec)

    def remap(self, remap: str) -> 'Vec2Map':
        new_map = self.clone()
        for i in range(len(new_map.vectors)):
            new_map.vectors[i] = new_map.vectors[i].remap(remap)
        return new_map

    def clone(self) -> 'Vec2Map':
        new_map = Vec2Map()
        for vec in self.vectors:
            new_map.append(vec.clone())
        return new_map

    def translate(self, translation) -> 'Vec2Map':
        new_map = self.clone()
        for i in range(len(new_map.vectors)):
            new_map.vectors[i] = new_map.vectors[i].add(translation)
        return new_map

    def match_points(self, other: 'Vec2Map'):
        self_vectors = self.vectors.copy()
        other_vectors = other.vectors.copy()
        matches = 0

        while True:
            found_match = False

            for self_v in self_vectors:
                for other_v in other_vectors:
                    if self_v.equal(other_v):
                        matches += 1
                        self_vectors.remove(self_v)
                        other_vectors.remove(other_v)
                        found_match = True
                        break
                if found_match:
                    break

            if not found_match:
                break

        return matches

    def __str__(self):
        result = ''
        for vec in self.vectors:
            result += f'{vec}\n'
        return result


remaps2 = []

for coords in ['xy', 'yx']:
    for signs in ['++', '-+', '+-', '--']:
        remap = ''
        for i in range(2):
            remap = remap + f'{signs[i]}{coords[i]}'
        remaps2.append(remap)


def part_one(in_file, out_file):
    scanners: list[Vec2Map] = []

    scanner = Vec2Map()
    scanner.append(Vec2(0, 2))
    # scanner.append(Vec2(4, 1))
    # scanner.append(Vec2(3, 3))
    scanners.append(scanner)

    scanner = Vec2Map()
    scanner.append(Vec2(-1, -1))
    # scanner.append(Vec2(-5, 0))
    # scanner.append(Vec2(-2, 1))
    scanners.append(scanner)

    for remap in remaps2:
        print('remap', remap)
        vecsb = scanners[1].remap(remap)
        for vecb in vecsb.vectors:
            for veca in scanners[0].vectors:
                translation = vecb.subtract(veca)
                print('translation', translation)
                tvecsb = vecsb.translate(translation)
                print(scanners[0])
                print(tvecsb)
                print()
                # matches = scanners[0].match_points(tvecsb)
                # if matches > 0:
                #     print(matches)


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
