import argparse
from dataclasses import dataclass


def part_one(in_file_name):
    in_file = open(in_file_name)
    positions = [int(v) for v in in_file.readline().strip().split(',')]

    max_pos = max(positions)
    least_fuel = None
    least_fuel_pos = None

    for pos in range(max_pos + 1):
        fuel_expenditure = [abs(positions[i] - pos) for i in range(len(positions))]
        total_expenditure = sum(fuel_expenditure)
        if least_fuel == None or total_expenditure < least_fuel:
            least_fuel = total_expenditure
            least_fuel_pos = pos

    print(least_fuel)


move_cache = dict()


def fuel_for_move(distance):
    cached = move_cache.get(distance)
    if cached != None:
        return cached

    fuel = sum(range(distance + 1))
    move_cache[distance] = fuel

    return fuel


def part_two(in_file_name):
    in_file = open(in_file_name)
    positions = [int(v) for v in in_file.readline().strip().split(',')]

    max_pos = max(positions)
    least_fuel = None

    for pos in range(max_pos + 1):
        fuel_expenditure = [fuel_for_move(abs(positions[i] - pos)) for i in range(len(positions))]
        total_expenditure = sum(fuel_expenditure)
        if least_fuel == None or total_expenditure < least_fuel:
            least_fuel = total_expenditure

    print(least_fuel)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 07')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
