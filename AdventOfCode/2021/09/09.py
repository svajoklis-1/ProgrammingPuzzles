import argparse
from dataclasses import dataclass
from functools import reduce


@dataclass
class Point:
    x: int
    y: int

    def to_idx(self, width):
        return self.y * width + self.x


class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.data = []

    def from_lines(lines):
        map = Map()
        lines = [line.strip() for line in lines]

        map.width = len(lines[0])
        map.height = len(lines)
        map.data = [int(point) for point in "".join(lines)]

        return map

    def get_adjacent(self, idx: int):
        x = int(idx % self.width)
        y = int(idx / self.width)

        adjacent = []
        if x > 0:
            adjacent.append(idx - 1)
        if x < self.width - 1:
            adjacent.append(idx + 1)
        if y > 0:
            adjacent.append(idx - self.width)
        if y < self.height - 1:
            adjacent.append(idx + self.width)

        return adjacent

    def copy(self):
        map = Map()
        map.width = self.width
        map.height = self.height
        map.data = self.data.copy()


def part_one(in_file_name):
    in_file = open(in_file_name, "r")
    map = Map.from_lines(in_file.readlines())

    risk_levels_sum = 0

    for idx in range(len(map.data)):
        adjacent = map.get_adjacent(idx)
        lower = True
        for adj in adjacent:
            lower = lower and map.data[idx] < map.data[adj]
        if lower:
            risk_levels_sum += map.data[idx] + 1

    print(risk_levels_sum)


def flood_fill_map(map: Map, idx: int):
    if map.data[idx] == 9:
        return 0

    map.data[idx] = 9

    sum_filled = 1
    for adj in map.get_adjacent(idx):
        sum_filled += flood_fill_map(map, adj)

    return sum_filled


def part_two(in_file_name):
    in_file = open(in_file_name, "r")
    map = Map.from_lines(in_file.readlines())

    basins = []

    for idx in range(len(map.data)):
        basin_size = flood_fill_map(map, idx)
        if basin_size > 0:
            basins.append(basin_size)

    basins.sort()
    print(reduce(lambda acc, v: acc * v, basins[-3:]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 09")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
