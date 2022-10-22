import argparse


class Submarine:
    def __init__(self):
        self.horizontal_position = 0
        self.depth = 0

    def dive(self, depth):
        self.depth += depth

    def move(self, distance):
        self.horizontal_position += distance


class Submarine2:
    def __init__(self):
        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0

    def down(self, amount):
        self.aim += amount

    def up(self, amount):
        self.aim -= amount

    def forward(self, amount):
        self.horizontal_position += amount
        self.depth += self.aim * amount


def part_one(in_file_name):
    sub = Submarine()

    in_file = open(in_file_name, "r")
    for line in in_file:
        command = [x.strip() for x in line.split(" ")]
        match command[0]:
            case "forward":
                sub.move(int(command[1]))
            case "down":
                sub.dive(int(command[1]))
            case "up":
                sub.dive(-int(command[1]))

    print(f"Depth: {sub.depth}")
    print(f"Distance: {sub.horizontal_position}")


def part_two(in_file_name):
    sub = Submarine2()

    in_file = open(in_file_name, "r")
    for line in in_file:
        command = [x.strip() for x in line.split(" ")]
        match command[0]:
            case "forward":
                sub.forward(int(command[1]))
            case "down":
                sub.down(int(command[1]))
            case "up":
                sub.up(int(command[1]))

    print(f"Depth: {sub.depth}")
    print(f"Distance: {sub.horizontal_position}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 02")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    match args.part:
        case "one":
            part_one(args.in_file)
        case "two":
            part_two(args.in_file)
