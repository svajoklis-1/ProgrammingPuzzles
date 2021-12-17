from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


@dataclass
class Insertion:
    left: str
    right: str
    insert: str


class Polymer:
    elements: list[str]

    def __init__(self, initial_elements):
        self.elements = initial_elements
        self.insertion_map = {}

    def add_insertion(self, insertion: Insertion):
        if insertion.left in self.insertion_map.keys():
            left = self.insertion_map[insertion.left]
        else:
            left = {}
            self.insertion_map[insertion.left] = left

        left[insertion.right] = insertion.insert

    def grow(self):
        i = 0
        while i < len(self.elements) - 1:
            left = self.elements[i]
            right = self.elements[i + 1]
            insert = self.insertion_map.get(left, {}).get(right, None)
            if insert:
                self.elements.insert(i + 1, insert)
                i += 1
            i += 1

    def __str__(self):
        return ''.join(self.elements)


def part_one(in_file_name):
    with open(in_file_name, 'r', encoding='utf-8') as in_file:
        polymer_elements = list(in_file.readline().strip())
        polymer = Polymer(polymer_elements)
        in_file.readline()
        while line := in_file.readline():
            line = line.strip()
            [pair, insert] = line.split(' -> ')
            [left, right] = list(pair)

            insertion = Insertion(left, right, insert)

            polymer.add_insertion(insertion)

    for i in range(10):
        polymer.grow()

    counts = {}
    for element in polymer.elements:
        counts[element] = counts.get(element, 0) + 1

    max_val = None
    min_val = None
    for value in counts.values():
        if max_val is None or value > max_val:
            max_val = value
        if min_val is None or value < min_val:
            min_val = value

    print(max_val - min_val)


class PolymerTwo:
    elements: list[str]

    def __init__(self, initial_elements):
        self.pairs = {}

        for i in range(len(initial_elements) - 1):
            key = f'{initial_elements[i]}{initial_elements[i + 1]}'
            self.pairs[key] = self.pairs.get(key, 0) + 1

        self.elements = {}
        for element in initial_elements:
            self.elements[element] = self.elements.get(element, 0) + 1

        self.insertions = {}

    def add_insertion(self, insertion: Insertion):
        key = f'{insertion.left}{insertion.right}'
        self.insertions[key] = insertion.insert

    def grow(self):
        new_pairs = {}
        for pair in self.pairs:
            insert = self.insertions.get(pair)
            if insert:
                self.elements[insert] = self.elements.get(insert, 0) + self.pairs[pair]
                new_pair_keys = [f'{pair[0]}{insert}', f'{insert}{pair[1]}']
                for new_pair in new_pair_keys:
                    new_pairs[new_pair] = new_pairs.get(new_pair, 0) + self.pairs[pair]
        self.pairs = new_pairs

    def __str__(self):
        return ''.join(self.elements)


def part_two(in_file_name):
    with open(in_file_name, 'r', encoding='utf-8') as in_file:
        polymer_elements = list(in_file.readline().strip())
        polymer = PolymerTwo(polymer_elements)
        in_file.readline()
        while line := in_file.readline():
            line = line.strip()
            [pair, insert] = line.split(' -> ')
            [left, right] = list(pair)

            insertion = Insertion(left, right, insert)

            polymer.add_insertion(insertion)

    for i in range(40):
        polymer.grow()

    print(polymer.elements)

    max_value = None
    min_value = None
    for value in polymer.elements.values():
        if max_value is None or value > max_value:
            max_value = value
        if min_value is None or value < min_value:
            min_value = value

    print(max_value - min_value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 14')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
