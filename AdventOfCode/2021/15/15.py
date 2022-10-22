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


class CaveMapNode:
    idx: int
    risk_level: int
    adjacent: list["CaveMapNode"]
    visited: False

    def __init__(self, idx, risk_level):
        self.idx = idx
        self.risk_level = risk_level
        self.adjacent = []
        self.visited = False

    def __str__(self):
        return f"Cave({self.idx})"


def node_risk_level(node: CaveMapNode):
    return node.risk_level


class CaveMap:
    width: int
    height: int
    data: list[int]
    start: CaveMapNode
    end: CaveMapNode

    @staticmethod
    def from_data(width: int, height: int, data: list[str]) -> "CaveMap":
        cave_map = CaveMap()
        cave_map.width = width
        cave_map.height = height
        cave_map.data = data
        return cave_map

    def build_tree(self):
        nodes_by_index = [None] * len(self.data)
        for idx in range(len(self.data)):
            nodes_by_index[idx] = CaveMapNode(idx, self.data[idx])
        self.start = nodes_by_index[0]
        self.end = nodes_by_index[len(self.data) - 1]

        for idx in range(len(self.data)):
            node = nodes_by_index[idx]
            adjacent_indexes = self.get_adjacent(idx)
            for adj in adjacent_indexes:
                node.adjacent.append(nodes_by_index[adj])

            node.adjacent.sort(key=node_risk_level)

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
        if free_up:
            adjacent.append(idx - self.width)
        if free_right:
            adjacent.append(idx + 1)
        if free_down:
            adjacent.append(idx + self.width)

        return adjacent


def d(current: CaveMapNode, neighbor: CaveMapNode):
    return neighbor.risk_level


def h(node: CaveMapNode, cave_map: CaveMap):
    idx_diff = cave_map.end.idx - node.idx
    return int(idx_diff / cave_map.width) + int(idx_diff % cave_map.width)


def find_current(open_set: set[CaveMapNode], f_score) -> CaveMapNode:
    min_f = INFINITY
    min_cave = None
    for cave in open_set:
        cave_f = f_score.get(cave, INFINITY)
        if cave_f < min_f:
            min_f = cave_f
            min_cave = cave

    return min_cave


def reconstruct_path(came_from: dict[CaveMapNode], current: CaveMapNode):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def walk(start: CaveMapNode, end: CaveMapNode, cave_map: CaveMap):
    open_set = set()
    open_set.add(start)

    came_from: dict[CaveMapNode] = dict()

    g_score: dict[CaveMapNode] = dict()  # default - None - infinitely big
    g_score[start] = 0

    f_score: dict[CaveMapNode] = dict()  # default - None - infinitely big
    f_score[start] = h(start, cave_map)

    while len(open_set) > 0:
        current = find_current(open_set, f_score)
        if current == end:
            path = reconstruct_path(came_from, current)
            weight_sum = 0
            for node in path[1:]:
                weight_sum += node.risk_level
            print(weight_sum)
            return

        open_set.remove(current)
        for neighbor in current.adjacent:
            tentative_g_score = g_score.get(current, INFINITY) + d(current, neighbor)
            if tentative_g_score < g_score.get(neighbor, INFINITY):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, cave_map)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    print("Failed to find path")


def part_one(in_file_name):
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        map_lines = [l.strip() for l in in_file.readlines()]
        width = len(map_lines[0])
        height = len(map_lines)
        data = [int(point) for line in map_lines for point in line]
        cave_map = CaveMap.from_data(width, height, data)
        cave_map.build_tree()
        walk(cave_map.start, cave_map.end, cave_map)


def part_two(in_file_name):
    with open(in_file_name, "r", encoding="utf-8") as in_file:
        map_lines = [l.strip() for l in in_file.readlines()]
        raw_width = len(map_lines[0])
        raw_height = len(map_lines)
        raw_data = [int(point) for line in map_lines for point in line]
        width = raw_width * 5
        height = raw_height * 5
        data = [0] * (width * height)
        for x in range(width):
            for y in range(height):
                idx = y * width + x
                data[idx] = raw_data[(y % raw_width) * raw_width + (x % raw_width)]
                add = int(y / raw_width) + int(x / raw_width)
                data[idx] = data[idx] + add
                while data[idx] > 9:
                    data[idx] -= 9

        cave_map = CaveMap.from_data(width, height, data)
        cave_map.build_tree()
        walk(cave_map.start, cave_map.end, cave_map)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 15")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
