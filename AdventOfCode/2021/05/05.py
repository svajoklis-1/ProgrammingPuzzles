import argparse
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def copy(self):
        return Point(self.x, self.y)


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.start} -> {self.end}'


class Field:
    def __init__(self, field_size: Point):
        self.field_size = field_size
        self.field = [0 for i in range(field_size.x * field_size.y)]

    def mark_line(self, line):
        x_step = 1 if line.end.x > line.start.x else (-1 if line.end.x < line.start.x else 0)
        y_step = 1 if line.end.y > line.start.y else (-1 if line.end.y < line.start.y else 0)

        cur_point = line.start.copy()

        while cur_point.x != line.end.x + x_step or cur_point.y != line.end.y + y_step:
            self.field[cur_point.y * self.field_size.x + cur_point.x] += 1
            cur_point.x += x_step
            cur_point.y += y_step


def find_max_point(lines):
    max_point = Point(0, 0)

    for line in lines:
        for point in [line.start, line.end]:
            if point.x > max_point.x:
                max_point.x = point.x
            if point.y > max_point.y:
                max_point.y = point.y

    return max_point


def read_lines(in_file):
    lines = []
    for coord_line in in_file:
        points = [p.strip() for p in coord_line.split(' -> ')]
        points = [[int(c) for c in point.split(',')] for point in points]
        line = Line(
            Point(points[0][0], points[0][1]),
            Point(points[1][0], points[1][1]),
        )
        lines.append(line)

    return lines


def part_one(in_file_name):
    in_file = open(in_file_name, 'r')
    lines = read_lines(in_file)
    lines = [l for l in lines if l.start.x == l.end.x or l.start.y == l.end.y]

    max_point = find_max_point(lines)

    field = Field(Point(max_point.x + 1, max_point.y + 1))

    for line in lines:
        field.mark_line(line)

    num_overlap = sum([1 for f in field.field if f >= 2])

    print(num_overlap)


def part_two(in_file_name):
    in_file = open(in_file_name, 'r')
    lines = read_lines(in_file)

    max_point = find_max_point(lines)

    field = Field(Point(max_point.x + 1, max_point.y + 1))

    for line in lines:
        field.mark_line(line)

    num_overlap = sum([1 for f in field.field if f >= 2])

    print(num_overlap)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 05')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
