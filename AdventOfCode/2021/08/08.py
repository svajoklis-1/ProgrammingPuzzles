'''
num 	num_digits 	idx		got
1		2			0		y

7		3			1		y

4		4			2		y

2		5			3
3		5			4
5		5			5

0		6			6
6		6			7
9		6			8		y

8		7			9		y
'''


import argparse
from dataclasses import dataclass


def len_key(a):
	return len(a)


def subtract_string(a, b):
	return ''.join([l for l in a if l not in b])


def part_one(in_file_name):
	in_file = open(in_file_name)

	for line in in_file:
		[segments, output] = [e.strip() for e in line.split('|')]
		segments = segments.split(' ')
		segments.sort(key=len_key)
		output = output.split(' ')

		digit_segments = dict()
		for i in range(10):
			digit_segments[i] = ''
		digit_segments[1] = segments[0]
		digit_segments[7] = segments[1]
		digit_segments[4] = segments[2]
		digit_segments[8] = segments[9]

		segments_by_len = dict()
		for i in range(8):
			segments_by_len[i] = []
		for segment in segments:
			segments_by_len[len(segment)].append(segment)

		segment_map = dict()
		for l in 'abcdefg':
			segment_map[l] = ''

		segment_map['a'] = subtract_string(digit_segments[7], digit_segments[1])
		for digits_6 in segments_by_len[6]:
			guess = digits_6
			for subtrahend in [digit_segments[1], digit_segments[7], digit_segments[4]]:
				guess = subtract_string(guess, subtrahend)
			if len(guess) == 1:
				segment_map['g'] = guess
				digit_segments[9] = digits_6
				segments_by_len[6].remove(digits_6)
				break

		segment_map['e'] = subtract_string(digit_segments[8], digit_segments[9])

		for digits_6 in segments_by_len[6]:
			guess = digits_6
			for subtrahend in [digit_segments[7], segment_map['g'], segment_map['e']]:
				guess = subtract_string(guess, subtrahend)
			if len(guess) == 1:
				digit_segments[0] = digits_6
				segment_map['b'] = guess
				segments_by_len[6].remove(digits_6)
				break

		# segment_map['c'] = subtract_string(digit_segments[0], digit_segments[6])


		print(segment_map)
		print(digit_segments)
		print(segments_by_len)
		print()




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
