from abc import abstractmethod
from typing import Union
from dataclasses import dataclass
import sys
import argparse

from typing import TextIO

# Import libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

INFINITY = 9223372036854775805

sys.path.append('../../../')


class CubeMap:
    size: int
    cube_map: list[list[list[int]]]

    def __init__(self, size: int):
        self.size = size
        self.cube_map = []
        for _x in range(size * 2 + 1):
            xa = []
            for _y in range(size * 2 + 1):
                ya = [0] * (size * 2 + 1)
                xa.append(ya)
            self.cube_map.append(xa)

    def set_values(self, rx: tuple[int, int], ry: tuple[int, int], rz: tuple[int, int], value: int):
        for z in range(rz[0], rz[1] + 1):
            if z < -self.size or z > self.size:
                continue
            for y in range(ry[0], ry[1] + 1):
                if y < -self.size or y > self.size:
                    continue
                for x in range(rx[0], rx[1] + 1):
                    if x < -self.size or x > self.size:
                        continue
                    self.cube_map[z + self.size][y + self.size][x + self.size] = value

    def count_on(self):
        count = 0
        for z in range(-self.size, self.size + 1):
            for y in range(-self.size, self.size + 1):
                for x in range(-self.size, self.size + 1):
                    if self.cube_map[z + self.size][y + self.size][x + self.size] == 1:
                        count += 1
        return count


@dataclass
class Point:
    x: int
    y: int
    z: int

    def less_than(self, other: 'Point') -> bool:
        return self.x < other.x or self.y < other.y or self.z < other.z


class AABB:
    start: Point
    end: Point

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.start} -> {self.end}'

    def get_volume(self) -> int:
        return (self.end.x - self.start.x) * (self.end.y - self.start.y) * (self.end.z - self.start.z)

    def subtract_aabb(self, other: 'AABB') -> list['AABB']:
        result: list[AABB] = []

        # -x side
        if other.start.x > self.start.x:
            start_x = self.start.x
            start_y = self.start.y
            start_z = self.start.z

            end_x = other.start.x
            end_y = self.end.y
            end_z = self.end.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        # +x side
        if other.end.x < self.end.x:
            start_x = other.end.x
            start_y = self.start.y
            start_z = self.start.z

            end_x = self.end.x
            end_y = self.end.y
            end_z = self.end.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        # -y side
        if self.start.y < other.start.y:
            start_x = max(self.start.x, other.start.x)
            start_y = self.start.y
            start_z = self.start.z

            end_x = min(self.end.x, other.end.x)
            end_y = other.start.y
            end_z = self.end.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        # +y side
        if self.end.y > other.end.y:
            start_x = max(self.start.x, other.start.x)
            start_y = other.end.y
            start_z = self.start.z

            end_x = min(self.end.x, other.end.x)
            end_y = self.end.y
            end_z = self.end.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        # -z side
        if self.start.z < other.start.z:
            start_x = max(self.start.x, other.start.x)
            start_y = max(self.start.y, other.start.y)
            start_z = self.start.z

            end_x = min(self.end.x, other.end.x)
            end_y = min(self.end.y, other.end.y)
            end_z = other.start.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        # +z side
        if self.end.z > other.end.z:
            start_x = max(self.start.x, other.start.x)
            start_y = max(self.start.y, other.start.y)
            start_z = other.end.z

            end_x = min(self.end.x, other.end.x)
            end_y = min(self.end.y, other.end.y)
            end_z = self.end.z

            start = Point(start_x, start_y, start_z)
            end = Point(end_x, end_y, end_z)
            result_box = AABB(start, end)
            if result_box.get_volume() > 0:
                result.append(result_box)

        return result

    def intersect(self, other: 'AABB') -> Union[None, 'AABB']:
        start_point = Point(
            max(self.start.x, other.start.x),
            max(self.start.y, other.start.y),
            max(self.start.z, other.start.z)
        )
        end_point = Point(
            min(self.end.x, other.end.x),
            min(self.end.y, other.end.y),
            min(self.end.z, other.end.z)
        )

        if end_point.less_than(start_point):
            return None

        return AABB(
            start_point,
            end_point
        )

    def __repr__(self):
        return f'AABB({self.start} -> {self.end})'


def read_instructions(in_file: TextIO) -> list[tuple[str, list[tuple[int, int]]]]:
    commands: list[tuple[str, list[tuple[int, int]]]] = []
    for line in in_file:
        line = line.strip()
        if line:
            [command, coords] = line.split(' ')
            axes = coords.split(',')
            ranges = []
            for axis in axes:
                axis = axis[2:]
                axis = axis.split('..')
                axis = [int(a) for a in axis]
                ranges.append((axis[0], axis[1]))
            commands.append((command, ranges))
    return commands


def part_one(in_file: TextIO, out_file: TextIO):
    commands = read_instructions(in_file)

    cube = CubeMap(50)

    for (command, ranges) in commands:
        print(command)
        print(ranges)
        cube.set_values(ranges[0], ranges[1], ranges[2], 1 if command == 'on' else 0)

    out_file.write(str(cube.count_on()))


def part_two(in_file: TextIO, out_file: TextIO):
    commands = read_instructions(in_file)

    boxes: list[AABB] = []
    for command, coords in commands:
        start = Point(coords[0][0], coords[1][0], coords[2][0])
        end = Point(coords[0][1] + 1, coords[1][1] + 1, coords[2][1] + 1)
        command_box = AABB(start, end)

        print(command)
        if command == 'on':
            command_boxes: list[AABB] = [command_box]
            new_command_boxes: list[AABB] = []
            for box in boxes:
                for command_box in command_boxes:
                    intersection = box.intersect(command_box)
                    if intersection:
                        new_command_boxes.extend(command_box.subtract_aabb(intersection))
                    else:
                        new_command_boxes.append(command_box)
                command_boxes = new_command_boxes
                new_command_boxes = []
            boxes.extend(command_boxes)
        elif command == 'off':
            new_boxes: list[AABB] = []
            for box in boxes:
                intersection = box.intersect(command_box)
                if intersection:
                    new_boxes.extend(box.subtract_aabb(command_box))
                else:
                    new_boxes.append(box)
            boxes = new_boxes

    out_file.write(str(sum([b.get_volume() for b in boxes])))


def test():
    tests = [
        (
            AABB(Point(-1, 1, 1), Point(2, 2, 2)),
            AABB(Point(0, 0, 0), Point(3, 3, 3)),
            25
        ),
        (
            AABB(Point(-1, -1, -1), Point(0, 0, 0)),
            AABB(Point(0, 0, 0), Point(3, 3, 3)),
            27
        ),
    ]

    for x in range(3):
        for y in range(3):
            for z in range(3):
                tests.append((
                    AABB(Point(x, y, z), Point(x + 1, y + 1, z + 1)),
                    AABB(Point(0, 0, 0), Point(3, 3, 3)),
                    26
                ))

    for x in range(0, 3):
        tests.append((
            AABB(Point(x, -99, -99), Point(x + 1, 99, 99)),
            AABB(Point(0, 0, 0), Point(3, 3, 3)),
            18
        ))

    for y in range(0, 3):
        tests.append((
            AABB(Point(-99, y, -99), Point(99, y + 1, 99)),
            AABB(Point(0, 0, 0), Point(3, 3, 3)),
            18
        ))

    for z in range(0, 3):
        tests.append((
            AABB(Point(-99, -99, z), Point(99, 99, z + 1)),
            AABB(Point(0, 0, 0), Point(3, 3, 3)),
            18
        ))

    tests.append((
        AABB(Point(1, 1, 1), Point(4, 4, 4)),
        AABB(Point(0, 0, 0), Point(3, 3, 3)),
        3**3 - 2**3
    ))

    for little_box, big_box, expected_volume in tests:
        new_total_volume = 0
        for box in big_box.subtract_aabb(little_box):
            new_total_volume += box.get_volume()

        ok = new_total_volume == expected_volume
        print('OK' if ok else 'FAIL')
        if not ok:
            print(f'Old total volume: {big_box.get_volume()}')
            print(f'New total volume: {new_total_volume}')


def main(file_name: str, part: str):
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
