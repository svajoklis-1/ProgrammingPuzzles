from io import FileIO
from os import stat
import sys
import argparse
from math import floor, ceil

from dataclasses import dataclass
from functools import reduce
from enum import Enum, auto

import re

INFINITY = 9223372036854775805

sys.path.append("../../../")
from util.term_control import (
    TermControl,
    TermColor,
)  # pylint: disable=wrong-import-position,import-error


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


num_re = re.compile(r"(\d+).*")


class SnailNode:
    parent: "SnailPair"

    def __init__(self):
        self.parent = None

    def find_splittable(self) -> "SnailValue":
        pass

    def get_magnitude(self) -> int:
        return 0

    def clone(self) -> "SnailNode":
        pass


class SnailValue(SnailNode):
    value: int

    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def get_leaves(self):
        return [self]

    def find_splittable(self):
        if self.value >= 10:
            return self
        return None

    def get_magnitude(self):
        return self.value

    def clone(self):
        return SnailValue(self.value)


class SnailPair(SnailNode):
    """
    Represents a single SnailPair of two sides.
    """

    left: SnailNode
    right: SnailNode

    def __init__(self, left=None, right=None):
        super().__init__()
        self.left = left
        if left:
            left.parent = self
        self.right = right
        if right:
            right.parent = self

    def __str__(self):
        left = self.left
        right = self.right

        return f"[{left},{right}]"

    def add(self, other: "SnailPair"):
        result = SnailPair()

        result.left = self
        result.left.parent = result
        result.right = other
        result.right.parent = result

        result.reduce()

        return result

    def reduce(self):
        while True:
            explodable = self.find_explodable()
            if explodable:
                explodable.explode()
                continue

            splittable = self.find_splittable()
            if splittable:
                new_pair = SnailPair(
                    SnailValue(floor(splittable.value / 2.0)),
                    SnailValue(ceil(splittable.value / 2.0)),
                )
                splittable.parent.replace(splittable, new_pair)
                continue

            break
        pass

    def find_splittable(self):
        return self.left.find_splittable() or self.right.find_splittable()

    def find_explodable(self, depth=0) -> "SnailPair":
        if depth == 3:
            if isinstance(self.left, SnailPair):
                return self.left
            if isinstance(self.right, SnailPair):
                return self.right

        result = isinstance(self.left, SnailPair) and self.left.find_explodable(
            depth + 1
        )
        if result:
            return result

        result = isinstance(self.right, SnailPair) and self.right.find_explodable(
            depth + 1
        )
        if result:
            return result

        return None

    def explode(self):
        new_val = SnailValue(0)
        new_val.parent = self.parent
        self.parent.replace(self, new_val)

        root = self
        while root.parent:
            root = root.parent

        leaves = root.get_leaves()
        new_idx = leaves.index(new_val)

        if new_idx > 0:
            leaves[new_idx - 1].value += self.left.value
        if new_idx < len(leaves) - 1:
            leaves[new_idx + 1].value += self.right.value

    def replace(self, what: SnailNode, replacement: SnailNode):
        if self.left == what:
            self.left = replacement
            replacement.parent = self
        elif self.right == what:
            self.right = replacement
            replacement.parent = self

    def get_leaves(self) -> list[SnailValue]:
        leaves = self.left.get_leaves() + self.right.get_leaves()
        return leaves

    def get_magnitude(self):
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def clone(self):
        result = SnailPair()
        result.left = self.left.clone()
        result.left.parent = result
        result.right = self.right.clone()
        result.right.parent = result
        return result


class SnailPairParser:
    string: str
    current_index: int

    def __init__(self, string):
        self.string = string
        self.current_index = 0

    def read_pair(self):
        char = self.peek_char()
        if char != "[":
            return None

        self.read_char()

        number = SnailPair()

        number.left = self.read_node()
        number.left.parent = number

        char = self.read_char()
        if char != ",":
            raise "Unexpected character, expected ,"

        number.right = self.read_node()
        number.right.parent = number

        char = self.read_char()
        if char != "]":
            raise "Unexpected character, expected ]"

        return number

    def read_value(self):
        num_match = num_re.match(self.string[self.current_index :])

        if not num_match:
            return None

        value_str = num_match.group(1)
        self.current_index += len(value_str)
        return SnailValue(int(value_str))

    def read_node(self):
        pair = self.read_pair()
        if pair:
            return pair

        value = self.read_value()
        if value:
            return value

        return None

    def peek_char(self):
        return self.string[self.current_index]

    def read_char(self):
        char = self.peek_char()
        self.current_index += 1
        return char


def part_one(in_file: FileIO, out_file: FileIO):
    num_string = in_file.readline().strip()
    snail_num = SnailPairParser(num_string).read_node()
    print(snail_num)
    while line := in_file.readline().strip():
        snail_num = snail_num.add(SnailPairParser(line).read_node())

    print(snail_num)
    out_file.write(str(snail_num.get_magnitude()))


def part_two(in_file: FileIO, out_file: FileIO):
    numbers: list[SnailPair] = []
    while num_string := in_file.readline().strip():
        numbers.append(SnailPairParser(num_string).read_node())

    for num in numbers:
        print(num)

    max_magnitude = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            i_num = numbers[i].clone()
            j_num = numbers[j].clone()

            num_sum = i_num.add(j_num)
            magnitude = num_sum.get_magnitude()
            if magnitude > max_magnitude:
                max_magnitude = magnitude

            i_num = numbers[i].clone()
            j_num = numbers[j].clone()

            num_sum = j_num.add(i_num)
            magnitude = num_sum.get_magnitude()
            if magnitude > max_magnitude:
                max_magnitude = magnitude

    out_file.write(str(max_magnitude))


def main(file_name, part):
    with open(f"{file_name}.in", "r", encoding="utf-8") as in_file:
        with open(f"{file_name}.{part}.out", "w", encoding="utf-8") as out_file:
            match part:
                case "one":
                    part_one(in_file, out_file)
                case "two":
                    part_two(in_file, out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 16")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    main(args.in_file, args.part)
