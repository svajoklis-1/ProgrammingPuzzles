import argparse
from dataclasses import dataclass
from functools import reduce


pairs = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]


error_values = {")": 3, "]": 57, "}": 1197, ">": 25137}


autocomplete_values = {")": 1, "]": 2, "}": 3, ">": 4}


def is_char_closing_for(a, b):
    for pair in pairs:
        if pair[1] == a and pair[0] == b:
            return True

    return False


def is_opening_char(char):
    return char in "([{<"


def is_closing_char(char):
    return char in ")]}>"


def get_opposite(char):
    for pair in pairs:
        if char == pair[0]:
            return pair[1]
        if char == pair[1]:
            return pair[0]


def print_pairs(counts):
    for pair in pairs:
        print(
            f"{pair[0]}:{pair[1]} = {counts.get(pair[0], 0)}:{counts.get(pair[1], 0)}"
        )


def is_line_corrupted(line):
    stack = []
    for char in line:
        if is_opening_char(char):
            stack.append(char)
            continue

        if not is_char_closing_for(char, stack[-1]):
            return True

        stack.pop()


def part_one(in_file_name):
    in_file = open(in_file_name, "r")
    lines = [list(line.strip()) for line in in_file.readlines()]

    error_score = 0

    for line in lines:
        stack = []
        for char in line:
            if is_opening_char(char):
                stack.append(char)
                continue

            if not is_char_closing_for(char, stack[-1]):
                print(f"Expected {get_opposite(stack[-1])}, but found {char} instead")
                error_score += error_values[char]
                break

            stack.pop()

    print(error_score)


def part_two(in_file_name):
    in_file = open(in_file_name, "r")
    lines = [list(line.strip()) for line in in_file.readlines()]

    autocomplete_scores = []

    for line in lines:
        if is_line_corrupted(line):
            continue

        stack = []
        for char in line:
            if is_opening_char(char):
                stack.append(char)
                continue

            stack.pop()

        stack = [get_opposite(char) for char in stack]
        stack.reverse()

        autocomplete_score = 0

        for char in stack:
            autocomplete_score *= 5
            autocomplete_score += autocomplete_values[char]

        autocomplete_scores.append(autocomplete_score)

    autocomplete_scores.sort()
    print(autocomplete_scores[int(len(autocomplete_scores) / 2)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 10")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
