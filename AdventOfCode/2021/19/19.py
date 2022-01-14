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
    '''
    Represents a two dimensional vector.
    '''

    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def clone(self) -> 'Vec2':
        '''Create a new copy of the vector.'''
        return Vec2(self.x, self.y)

    def remap(self, remap: str) -> 'Vec2':
        '''Returns a new vector where coordinates have been remapped with remap.'''
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
        '''Returns a new vector with result of `self - other`.'''
        return Vec2(self.x - other.x, self.y - other.y)

    def add(self, other: 'Vec2'):
        '''Returns a new vector with result of `self + other`.'''
        return Vec2(self.x + other.x, self.y + other.y)

    def equal(self, other: 'Vec2'):
        '''Returns true if vectors are equal.'''
        return self.x == other.x and self.y == other.y

    def distance_to(self, other):
        '''Returns distance between vectors.'''
        return sqrt(pow(self.x - other.x, 2), pow(self.y - other.y, 2))


class Vec2Map:
    '''
        Represents a vector map.
    '''
    vectors: list[Vec2]
    origin: Vec2

    def __init__(self):
        self.vectors = []
        self.origin = Vec2(0, 0)

    def append(self, vec: Vec2):
        '''Appends vector to end of vector map.'''
        self.vectors.append(vec)

    def remap(self, remap: str) -> 'Vec2Map':
        '''Creates a new vector map with `remap` applied to all vectors.'''
        new_map = self.clone()
        for (i, _) in enumerate(new_map.vectors):
            new_map.vectors[i] = new_map.vectors[i].remap(remap)
        new_map.origin = new_map.origin.remap(remap)
        return new_map

    def clone(self) -> 'Vec2Map':
        '''Creates a new copy of the vector map.'''
        new_map = Vec2Map()
        for vec in self.vectors:
            new_map.append(vec.clone())
        new_map.origin = self.origin.clone()
        return new_map

    def translate(self, translation: Vec2) -> 'Vec2Map':
        '''Creates a new copy of the vector map with all vectors translated by `translation`.'''
        new_map = self.clone()
        for (i, _) in enumerate(new_map.vectors):
            new_map.vectors[i] = new_map.vectors[i].add(translation)
        new_map.origin = new_map.origin.add(translation)
        return new_map

    def match_points(self, other: 'Vec2Map'):
        '''Returns a number of vectors that have an equal vector in `other`.'''
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


def make_remaps():
    '''Creates a list of 2d remaps.'''
    remaps = []

    for coords in ['xy', 'yx']:
        for signs in ['++', '-+', '+-', '--']:
            remap = ''
            for i in range(2):
                remap = remap + f'{signs[i]}{coords[i]}'
            remaps.append(remap)

    return remaps


def part_one(in_file, out_file):
    remaps = make_remaps()

    scanners: list[Vec2Map] = []

    scanner = Vec2Map()
    scanner.append(Vec2(0, 2))
    scanner.append(Vec2(4, 1))
    scanner.append(Vec2(3, 3))
    scanners.append(scanner)

    scanner = Vec2Map()
    scanner.append(Vec2(-1, -1))
    scanner.append(Vec2(-5, 0))
    scanner.append(Vec2(-2, 1))
    scanners.append(scanner)

    for remap in remaps:
        vecsb = scanners[1].remap(remap)
        for vecb in vecsb.vectors:
            for veca in scanners[0].vectors:
                translation = veca.subtract(vecb)
                tvecsb = vecsb.translate(translation)
                matches = scanners[0].match_points(tvecsb)
                if matches > 1:
                    print('remap', remap)
                    print('b origin', tvecsb.origin)
                    print(matches)
        print()


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
