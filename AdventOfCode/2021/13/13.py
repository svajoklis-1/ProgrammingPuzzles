from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

sys.path.append("../../../")
from util.term_control import (
    TermControl,
    TermColor,
)  # pylint: disable=wrong-import-position,import-error


@dataclass
class Dot:
    x: int
    y: int


class Dots:
    dots: list[Dot]

    def __init__(self):
        self.dots = []

    def append(self, dot):
        self.dots.append(dot)

    def fold(self, axis, coord):
        for dot in self.dots:
            self.fold_dot(dot, axis, coord)

    def fold_dot(self, dot, axis, coord):
        match axis:
            case "x":
                if dot.x == coord:
                    self.dots.remove(dot)
                    return
                if dot.x > coord:
                    dot.x = coord - (dot.x - coord)
            case "y":
                if dot.y == coord:
                    self.dots.remove(dot)
                    return
                if dot.y > coord:
                    dot.y = coord - (dot.y - coord)

    def make_unique(self):
        unique_dots = []
        for dot in self.dots:
            if dot not in unique_dots:
                unique_dots.append(dot)
        self.dots = unique_dots

    def print(self):
        max_x = 0
        max_y = 0
        for dot in self.dots:
            if dot.x > max_x:
                max_x = dot.x
            if dot.y > max_y:
                max_y = dot.y

        output = []
        for y in range(max_y + 1):
            output.append(" " * (max_x + 1))

        for dot in self.dots:
            line = list(output[dot.y])
            line[dot.x] = "*"
            output[dot.y] = "".join(line)

        for line in output:
            print(line)


def part_one(in_file_name):
    dots = Dots()
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        while line := in_file.readline().strip():
            [x, y] = [int(c) for c in line.split(",")]
            dots.append(Dot(x, y))

        while line := in_file.readline().strip():
            line = line.lstrip("fold along ").split("=")
            axis = line[0]
            coord = int(line[1])

            dots.fold(axis, coord)
            break

    dots.make_unique()
    print(len(dots.dots))


def part_two(in_file_name):
    dots = Dots()
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        while line := in_file.readline().strip():
            [x, y] = [int(c) for c in line.split(",")]
            dots.append(Dot(x, y))

        while line := in_file.readline().strip():
            line = line.lstrip("fold along ").split("=")
            axis = line[0]
            coord = int(line[1])

            dots.fold(axis, coord)

    dots.make_unique()
    dots.print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 13")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
