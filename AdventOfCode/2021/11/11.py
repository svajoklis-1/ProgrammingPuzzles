import argparse
from dataclasses import dataclass
from functools import reduce
import colorama


class Map:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.data = []
        self.reset()
        self.num_flashes = 0
        self.all_flashed = False
        self.tick_num = 0

    def from_lines(lines):
        map = Map()

        map.width = len(lines[0].strip())
        map.height = len(lines)
        map.data = [int(data) for data in ''.join([line.strip() for line in lines])]
        map.reset()

        return map

    def reset(self):
        self.flashed = [False] * len(self.data)

    def get_adjacent(self, idx: int):
        x = int(idx % self.width)
        y = int(idx / self.width)

        free_left = x > 0
        free_right = x < self.width - 1
        free_up = y > 0
        free_down = y < self.height - 1

        adjacent = []

        if free_left:
            adjacent.append(idx - 1)
        if free_left and free_up:
            adjacent.append(idx - 1 - self.width)
        if free_up:
            adjacent.append(idx - self.width)
        if free_up and free_right:
            adjacent.append(idx - self.width + 1)
        if free_right:
            adjacent.append(idx + 1)
        if free_right and free_down:
            adjacent.append(idx + 1 + self.width)
        if free_down:
            adjacent.append(idx + self.width)
        if free_down and free_left:
            adjacent.append(idx - 1 + self.width)

        return adjacent

    def check_flash(self, idx):
        if not self.flashed[idx] and self.data[idx] > 9:
            self.flashed[idx] = True
            self.num_flashes += 1
            self.data[idx] = 0
            adjacent = self.get_adjacent(idx)
            for adj in adjacent:
                if not self.flashed[adj]:
                    self.data[adj] += 1

            for adj in adjacent:
                self.check_flash(adj)

    def tick(self):
        self.tick_num += 1

        for idx in range(len(self.data)):
            self.data[idx] += 1
        for idx in range(len(self.data)):
            self.check_flash(idx)

        if len([flashed for flashed in self.flashed if flashed]) == len(self.flashed):
            self.all_flashed = True

        self.reset()

    def print(self):
        for pointi, point in enumerate(self.data):
            if point == 0:
                print(colorama.Style.BRIGHT + colorama.Fore.CYAN, end='')
            else:
                print(colorama.Style.DIM + colorama.Fore.WHITE, end='')
            print(point, end='')
            print(colorama.Style.RESET_ALL, end='')
            if pointi % self.width == self.width - 1:
                print()

        print()

    def print_pretty(self):
        for pointi, point in enumerate(self.data):
            if point == 0:
                print(colorama.Style.BRIGHT + colorama.Fore.CYAN + '*', end='')
            else:
                print(colorama.Style.DIM + colorama.Fore.WHITE + '_', end='')
            print(colorama.Style.RESET_ALL, end='')
            if pointi % self.width == self.width - 1:
                print()

        print()


def part_one(in_file_name):
    in_file = open(in_file_name, 'r')

    map = Map.from_lines(in_file.readlines())
    for i in range(100):
        map.tick()
    print(map.num_flashes)


def part_two(in_file_name):
    in_file = open(in_file_name, 'r')

    map = Map.from_lines(in_file.readlines())
    map.print_pretty()
    input()
    while not map.all_flashed:
        map.tick()
        map.print_pretty()
        input()
    print(map.tick_num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 11')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
