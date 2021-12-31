from io import FileIO
from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum, auto as iota

import re

INFINITY = 9223372036854775805

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


class Direction(Enum):
    LEFT = iota()
    RIGHT = iota()


num_re = re.compile(r'(\d+).*')


class SnailNumber:
    '''
    Represents a single SnailNumber of two sides.
    If a side is a SnailNumber *_number is the number and *_value is None.
    If a side is a value *_number is None and *_value is the value.
    '''
    left_number: 'SnailNumber'
    right_number: 'SnailNumber'

    left_value: int
    right_value: int

    parent: 'SnailNumber'

    def __init__(self):
        self.left_number = None
        self.right_number = None

        self.left_value = None
        self.right_value = None

        self.parent = None

    def __str__(self):
        left = self.left_number
        if not left:
            left = self.left_value

        right = self.right_number
        if not right:
            right = self.right_value

        return f'[{left},{right}]'

    def add(self, other):
        result = SnailNumber()

        result.left_number = self
        result.left_number.parent = result
        result.right_number = other
        result.right_number.parent = result

        result.reduce()

        return result

    def reduce(self):
        while True:
            explodable = self.find_explodable()
            if explodable:
                explodable.explode()
                continue

            break
        pass

    def find_explodable(self, depth=0) -> 'SnailNumber':
        if depth == 3:
            if self.left_number:
                return self.left_number
            if self.right_number:
                return self.right_number

        result = self.left_number and self.left_number.find_explodable(depth + 1)
        if result:
            return result

        result = self.right_number and self.right_number.find_explodable(depth + 1)
        if result:
            return result

        return None

    def explode(self):
        # add to the left
        # add to the right

        if self == self.parent.left_number:
            self.parent.left_number = None
            self.parent.left_value = 0
        if self == self.parent.right_number:
            self.parent.right_number = None
            self.parent.right_value = 0


class SnailNumberParser:
    string: str
    current_index: int

    def __init__(self, string):
        self.string = string
        self.current_index = 0

    def read_number(self):
        char = self.read_char()
        if char != '[':
            raise 'Unexpected character, expected ['

        number = SnailNumber()

        if self.peek_char() == '[':
            number.left_number = self.read_number()
            number.left_number.parent = number
        else:
            number.left_value = self.read_value()

        char = self.read_char()
        if char != ',':
            raise 'Unexpected character, expected ,'

        if self.peek_char() == '[':
            number.right_number = self.read_number()
            number.right_number.parent = number
        else:
            number.right_value = self.read_value()

        char = self.read_char()
        if char != ']':
            raise 'Unexpected character, expected ]'

        return number

    def read_value(self):
        num_match = num_re.match(self.string[self.current_index:])
        if num_match:
            value_str = num_match.group(1)
            self.current_index += len(value_str)
            return int(value_str)

        raise 'Expected to read a numerical value'

    def peek_char(self):
        return self.string[self.current_index]

    def read_char(self):
        char = self.peek_char()
        self.current_index += 1
        return char


def part_one(in_file: FileIO, out_file: FileIO):
    num_string = in_file.readline().strip()
    parser = SnailNumberParser(num_string)
    snail_num = parser.read_number()
    print(snail_num)
    print(snail_num.reduce())
    print(snail_num)


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
