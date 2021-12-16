import sys
import argparse

from dataclasses import dataclass
from functools import reduce

sys.path.append('../../../')

from util.term_control import TermControl, TermColor # pylint: disable=wrong-import-position,import-error


class Cave:
	def __init__(self, name):
		self.name = name
		self.adjacent = []


	def append_adjacent(self, cave):
		if not cave in self.adjacent:
			self.adjacent.append(cave)


class CaveMap:
	def __init__(self):
		self.cave_by_name = {}


def part_one(in_file_name):
	with open(in_file_name, 'r', encoding='utf-8') as in_file:
		cave_map = CaveMap()
		for line in in_file:
			[name_a, name_b] = line.strip().split('-')
			cave_a = cave_map.cave_by_name.get(cave_a, Cave(name_a))
			cave_b = cave_map.cave_by_name.get(cave_b, Cave(name_b))


def part_two(in_file_name):
	with open(in_file_name, 'r') as in_file:
		pass


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Puzzle 12')
	parser.add_argument('--part', choices=['one', 'two'], required=True)
	parser.add_argument('in_file')
	args = parser.parse_args()

	match args.part:
		case 'one':
			part_one(args.in_file)
		case 'two':
			part_two(args.in_file)
