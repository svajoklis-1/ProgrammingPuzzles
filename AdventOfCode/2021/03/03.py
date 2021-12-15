import argparse


def part_one(in_file_name):
  in_file = open(in_file_name, 'r')
  line = in_file.readline().strip()
  num_digits = len(line)

  ones = [0 for i in range(num_digits)]
  zeroes = [0 for i in range(num_digits)]

  lines = [l.strip() for l in [line] + list(in_file.readlines())]
  for line in lines:
    for digiti, digit in enumerate(line):
      if digit == '1':
        ones[digiti] += 1
      else:
        zeroes[digiti] += 1

  gamma = [] # most common
  sigma = [] # least common
  for i in range(num_digits):
    if ones[i] > zeroes[i]:
      gamma.append('1')
      sigma.append('0')
    else:
      gamma.append('0')
      sigma.append('1')

  gamma = int(''.join(gamma), 2)
  sigma = int(''.join(sigma), 2)

  print(f'Gamma: {gamma}')
  print(f'Sigma: {sigma}')


def most_common_digit(lines, checked_digit):
  ones = 0
  zeroes = 0

  for line in lines:
    digit = line[checked_digit]
    if digit == '1':
      ones += 1
    else:
      zeroes += 1

  return '1' if ones >= zeroes else '0'


def part_two(in_file_name):
  in_file = open(in_file_name, 'r')
  line = in_file.readline().strip()
  num_digits = len(line)


  lines = [l.strip() for l in [line] + list(in_file.readlines())]
  oxygen_lines = lines
  scrubber_lines = lines

  for i in range(num_digits):
    common_oxygen_digit = most_common_digit(oxygen_lines, i)
    if len(oxygen_lines) > 1:
      oxygen_lines = [l for l in oxygen_lines if l[i] == common_oxygen_digit]

    common_scrubber_digit = most_common_digit(scrubber_lines, i)
    if len(scrubber_lines) > 1:
      scrubber_lines = [l for l in scrubber_lines if l[i] != common_scrubber_digit]

  print('Oxygen:', int(oxygen_lines[0], 2))
  print('Scrubber:', int(scrubber_lines[0], 2))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Puzzle 03')
  parser.add_argument('--part', choices=['one', 'two'], required=True)
  parser.add_argument('in_file')
  args = parser.parse_args()

  match args.part:
    case 'one':
      part_one(args.in_file)
    case 'two':
      part_two(args.in_file)
