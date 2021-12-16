import argparse
from dataclasses import dataclass
from functools import reduce
import colorama

colorama.ansi.clear_screen()


def part_one(in_file_name):
	in_file = open(in_file_name, 'r')



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Puzzle 10')
	parser.add_argument('--part', choices=['one', 'two'], required=True)
	parser.add_argument('in_file')
	args = parser.parse_args()

	match args.part:
		case 'one':
			part_one(args.in_file)
			print(colorama.Style.BRIGHT + colorama.Fore.CYAN + 'OK' + colorama.Style.RESET_ALL)
		case 'two':
			part_two(args.in_file)
