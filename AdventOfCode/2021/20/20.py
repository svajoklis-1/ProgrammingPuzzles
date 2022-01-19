import sys
import argparse

from typing import TextIO

INFINITY = 9223372036854775805

sys.path.append('../../../')


class Image:
    '''Represents image captured by the scanners.'''
    size: int
    data: str
    surrounding: str

    def __init__(self, size: int):
        self.size = size
        self.data = "." * (size * size)
        self.surrounding = "."

    def set_data(self, data: str) -> 'Image':
        '''Sets data of the image. Data must be of compatible size for the image.'''
        assert len(data) == self.size * self.size,\
            "Trying to set Image data with mistmatched new data"
        self.data = data
        return self

    def get_area_around(self, target_x: int, target_y: int) -> str:
        '''Returns array of 9 data points around provided coordinates in a string format.'''
        result_chars = []
        for y in range(target_y - 1, target_y + 2):
            for x in range(target_x - 1, target_x + 2):
                if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
                    result_chars.append(self.surrounding)
                else:
                    result_chars.append(self.data[y * self.size + x])

        return "".join(result_chars)

    def enhance(self, algorithm: str) -> 'Image':
        '''Performs the enhancement using the provided algorithm.
        Returns new image with the algorithm applied.'''
        new_image = Image(self.size + 4)
        new_data = list(new_image.data)
        for row in range(new_image.size):
            for col in range(new_image.size):
                area = self.get_area_around(col - 2, row - 2)
                index = area_to_index(area)
                new_data[row * new_image.size + col] = algorithm[index]

        new_image.surrounding = new_data[0]

        new_image.set_data("".join(new_data))

        return new_image

    def print(self) -> None:
        '''Prints image to console output.'''
        for y in range(self.size):
            print(self.data[(y * self.size):((y + 1) * self.size)])


def area_to_index(area: str) -> int:
    '''Converts area of 9 points into an index into the algorithm. Returns index.'''
    result = 0
    for i in range(len(area)):
        result += (1 if area[-(i + 1)] == '#' else 0) * (2 ** i)
    return result


def read_data(in_file: TextIO) -> tuple[str, Image]:
    '''Reads image and algorithm from the input file. Returns (algorithm, image)'''
    algorithm = in_file.readline().strip()
    in_file.readline()
    first_line = in_file.readline().strip()
    size = len(first_line)
    lines = [first_line]
    for _i in range(size - 1):
        line = in_file.readline().strip()
        lines.append(line)
    image = Image(size)
    image.set_data("".join(lines))
    return (algorithm, image)


def part_one(in_file: TextIO, out_file: TextIO):
    (algorithm, image) = read_data(in_file)
    image = image.enhance(algorithm)
    image = image.enhance(algorithm)
    out_file.write(str(len([c for c in image.data if c == "#"])))


def part_two(in_file: TextIO, out_file: TextIO):
    (algorithm, image) = read_data(in_file)
    for _i in range(50):
        image = image.enhance(algorithm)
    out_file.write(str(len([c for c in image.data if c == "#"])))


def main(file_name: str, part: str):
    with open(f'{file_name}.in', 'r', encoding='utf-8') as in_file:
        with open(f'{file_name}.{part}.out', 'w', encoding='utf-8') as out_file:
            match part:
                case 'one':
                    part_one(in_file, out_file)
                case 'two':
                    part_two(in_file, out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 16')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    main(args.in_file, args.part)
