from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


class CaveSize(Enum):
    SMALL = 0
    LARGE = 1


class Cave:
    name: str
    adjacent: list
    size: CaveSize

    def __init__(self, name: str):
        self.name = name
        self.adjacent = []
        self.size = CaveSize.SMALL if name.islower() else CaveSize.LARGE

    def append_adjacent(self, cave):
        if not cave in self.adjacent:
            self.adjacent.append(cave)


class CaveMap:
    cave_by_name: dict[Cave]

    def __init__(self):
        self.cave_by_name = {}

    @staticmethod
    def from_lines(lines):
        map = CaveMap()
        for line in lines:
            [name_a, name_b] = line.strip().split('-')
            cave_a = map.cave_by_name.get(name_a)
            if not cave_a:
                cave_a = Cave(name_a)
                map.cave_by_name[name_a] = cave_a

            cave_b = map.cave_by_name.get(name_b)
            if not cave_b:
                cave_b = Cave(name_b)
                map.cave_by_name[name_b] = cave_b

            cave_a.append_adjacent(cave_b)
            cave_b.append_adjacent(cave_a)

        return map


def walk(cave: Cave, stack):
    for adj in cave.adjacent:
        if adj.name == 'end':
            print(stack)

        if adj not in stack:
            walk()


def part_one(in_file_name):
    with open(in_file_name, 'r', encoding='utf-8') as in_file:
        cave_map = CaveMap.from_lines(in_file.readlines())

        walk(cave_map.cave_by_name['start'], [])


def part_two(in_file_name):
    with open(in_file_name, 'r') as in_file:
        pass


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
