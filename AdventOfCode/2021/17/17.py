from io import FileIO
from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

INFINITY = 9223372036854775805

sys.path.append("../../../")
from util.term_control import (
    TermControl,
    TermColor,
)  # pylint: disable=wrong-import-position,import-error


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Area:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def has_point(self, point: Point):
        return (
            point.x >= self.x_min
            and point.x <= self.x_max
            and point.y >= self.y_min
            and point.y <= self.y_max
        )

    def has_passed(self, point: Point):
        return point.x > self.x_max or point.y < self.y_min


def check_if_hits_target(vxi: int, vyi: int, area: Area):
    vx = vxi
    vy = vyi
    position = Point(0, 0)

    while not area.has_passed(position):
        if area.has_point(position):
            return True

        position.x += vx
        position.y += vy
        vx = max(vx - 1, 0)
        vy = vy - 1

    return False


def part_one(in_file: FileIO, out_file: FileIO):
    target_spec = in_file.readline()
    target_spec = target_spec.strip().lstrip("target area: ")
    coords = [c.split("=") for c in target_spec.split(", ")]
    for coord in coords:
        coord[1] = coord[1].split("..")

    x_min = int(coords[0][1][0])
    x_max = int(coords[0][1][1])
    y_min = int(coords[1][1][0])
    y_max = int(coords[1][1][1])

    area = Area(x_min, x_max, y_min, y_max)

    vy = 77
    y = 0

    while True:
        print("y", y)
        print("vy", vy)

        input()

        y += vy
        vy -= 1

    print(highest_vyi)
    print(highest_y)


def part_two(in_file: FileIO, out_file: FileIO):
    target_spec = in_file.readline()
    target_spec = target_spec.strip().lstrip("target area: ")
    coords = [c.split("=") for c in target_spec.split(", ")]
    for coord in coords:
        coord[1] = coord[1].split("..")

    x_min = int(coords[0][1][0])
    x_max = int(coords[0][1][1])
    y_min = int(coords[1][1][0])
    y_max = int(coords[1][1][1])

    area = Area(x_min, x_max, y_min, y_max)
    print(area)

    count = 0
    for vxi in range(0, x_max + 1):
        for vyi in range(y_min, -y_min + 1):
            if check_if_hits_target(vxi, vyi, area):
                print(vxi, ",", vyi)
                count += 1

    print("Total:", count)


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
