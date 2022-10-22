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


class CaveSize(Enum):
    SMALL = 0
    LARGE = 1


class Cave:
    name: str
    adjacent: list
    size: CaveSize
    times_visited: int

    def __init__(self, name: str):
        self.name = name
        self.adjacent = []
        self.size = CaveSize.SMALL if name.islower() else CaveSize.LARGE
        match self.size:
            case CaveSize.SMALL:
                self.visits_left = 1
            case CaveSize.LARGE:
                self.visits_left = None
        self.times_visited = 0

    def append_adjacent(self, cave):
        if not cave in self.adjacent:
            self.adjacent.append(cave)

    def __str__(self):
        return f"Cave({self.name})"

    def __repr__(self):
        return self.__str__()


class CaveMap:
    cave_by_name: dict[Cave]

    def __init__(self):
        self.cave_by_name = {}

    @staticmethod
    def from_lines(lines):
        cave_map = CaveMap()
        for line in lines:
            [name_a, name_b] = line.strip().split("-")
            cave_a = cave_map.cave_by_name.get(name_a)
            if not cave_a:
                cave_a = Cave(name_a)
                cave_map.cave_by_name[name_a] = cave_a

            cave_b = cave_map.cave_by_name.get(name_b)
            if not cave_b:
                cave_b = Cave(name_b)
                cave_map.cave_by_name[name_b] = cave_b

            cave_a.append_adjacent(cave_b)
            cave_b.append_adjacent(cave_a)

        return cave_map


def walk(cave: Cave, stack: list[Cave], state):
    stack.append(cave)
    cave.times_visited += 1

    if cave.name == "end":
        state["ends"] += 1
    else:
        for adj in cave.adjacent:
            if adj.size == CaveSize.LARGE or adj.times_visited == 0:
                walk(adj, stack, state)

    stack.pop()
    cave.times_visited -= 1


def should_visit_adjacent_two(adj, state):
    if adj.name == "start":
        return False

    if adj.name == "end":
        return True

    match adj.size:
        case CaveSize.SMALL:
            if state["visited_small_cave_twice"]:
                return adj.times_visited < 1
            else:
                return adj.times_visited < 2
        case CaveSize.LARGE:
            return True


def walk_two(cave: Cave, stack: list[Cave], state):
    stack.append(cave)
    cave.times_visited += 1

    visited_this_twice = cave.size == CaveSize.SMALL and cave.times_visited == 2
    if visited_this_twice:
        state["visited_small_cave_twice"] = True

    if cave.name == "end":
        state["ends"] += 1
    else:
        for adj in cave.adjacent:
            if should_visit_adjacent_two(adj, state):
                walk_two(adj, stack, state)

    if visited_this_twice:
        state["visited_small_cave_twice"] = False
    stack.pop()
    cave.times_visited -= 1


def part_one(in_file_name):
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        cave_map = CaveMap.from_lines(in_file.readlines())
        state = {"ends": 0}

        walk(cave_map.cave_by_name["start"], [], state)

        print(state["ends"])


def part_two(in_file_name):
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        cave_map = CaveMap.from_lines(in_file.readlines())

        state = {"ends": 0, "visited_small_cave_twice": False}

        walk_two(cave_map.cave_by_name["start"], [], state)

        print(state["ends"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 12")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
