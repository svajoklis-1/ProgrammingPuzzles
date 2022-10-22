import argparse
from dataclasses import dataclass


class Fish:
    def __init__(self, initial):
        self.state = initial
        self.day = 0

    def next_day(self):
        self.day += 1

        num_new_fish = 0
        for i in range(len(self.state)):
            f = self.state[i]
            if f == 0:
                self.state[i] = 6
                num_new_fish += 1
                continue

            self.state[i] = f - 1

        self.state = self.state + [8] * num_new_fish

    def print(self):
        label = "Initial state"
        if self.day > 0:
            label = f"After {self.day} days"

        print(f"{label}: {self.state}")


def part_one(in_file_name):
    in_file = open(in_file_name, "r")
    fish = Fish([int(v) for v in in_file.readline().strip().split(",")])

    fish.print()
    for i in range(256):
        fish.next_day()

    print("Fish in total: ", len(fish.state))


class FishSums:
    def __init__(self, initial):
        self.day = 0
        self.counts = [0] * 9
        for i in initial:
            self.counts[i] += 1

    def next_day(self):
        self.day += 1

        last_0 = self.counts[0]
        for i in range(1, 9):
            self.counts[i - 1] = self.counts[i]
        self.counts[8] = 0

        self.counts[6] += last_0
        self.counts[8] += last_0

    def print(self):
        label = "Initial state"
        if self.day > 0:
            label = f"After {self.day} days"

        print(f"{label}: {self.counts}, total: {sum(self.counts)}")


def part_two(in_file_name):
    in_file = open(in_file_name, "r")
    fish = FishSums([int(v) for v in in_file.readline().strip().split(",")])

    fish.print()
    for i in range(256):
        fish.next_day()
        fish.print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 06")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
