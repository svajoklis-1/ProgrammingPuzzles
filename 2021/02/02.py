import argparse


class Submarine:
  def __init__(self):
    self.horizontal_position = 0
    self.depth = 0

  def perform_command():
    pass


def part_one(in_file_name):
  pass


def part_two(in_file_name):
  pass


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Puzzle 02')
  parser.add_argument('--part', choices=['one', 'two'], required=True)
  parser.add_argument('in_file')
  args = parser.parse_args()

  match args.part:
    case 'one':
      part_one(args.in_file)
    case 'two':
      part_two(args.in_file)
