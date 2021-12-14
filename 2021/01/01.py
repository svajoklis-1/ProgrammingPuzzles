import argparse

def part_one(in_file_name):
  in_file = open(in_file_name, 'r')
  num_increased = 0
  last_depth = None
  for reading in in_file:
    cur_depth = int(reading)
    if last_depth == None:
      last_depth = cur_depth
      continue

    if cur_depth > last_depth:
      num_increased += 1

    last_depth = cur_depth

  in_file.close()

  print(num_increased)


def part_two(in_file_name):
  in_file = open(in_file_name, 'r')

  depths = []
  num_increased = 0
  prev_sum = 0

  for reading in in_file:
    cur_depth = int(reading)

    if len(depths) < 3:
      depths.append(cur_depth)
      continue
    elif len(depths) == 3:
      prev_sum = sum(depths)

    depths = depths[1:] + [cur_depth]
    cur_sum = sum(depths)

    if cur_sum > prev_sum:
      num_increased += 1

    prev_sum = cur_sum

  print(num_increased)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Puzzle 01')
  parser.add_argument('--part', choices=['one', 'two'], required=True)
  parser.add_argument('in_file')
  args = parser.parse_args()

  match args.part:
    case 'one':
      part_one(args.in_file)
    case 'two':
      part_two(args.in_file)
