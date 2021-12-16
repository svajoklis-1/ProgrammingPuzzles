'''
num 	num_digits 	idx		got
1		2			0		y

7		3			1		y

4		4			2		y

2		5			3
3		5			4
5		5			5

0		6			6		y
6		6			7		y
9		6			8		y

8		7			9		y
'''


import argparse
from dataclasses import dataclass


def len_key(a):
    return len(a)


def subtract_string(a, b):
    return ''.join([l for l in a if l not in b])


def subtract_strings(minuend, strings):
    for string in strings:
        minuend = subtract_string(minuend, string)
    return minuend


def are_strings_equal(a, b):
    if len(a) > len(b):
        return len(subtract_string(a, b)) == 0
    else:
        return len(subtract_string(b, a)) == 0


def build_segments_by_digit(segments):
    segments_by_digit = dict()
    for i in range(10):
        segments_by_digit[i] = ''

    segments_by_len = dict()
    for i in range(8):
        segments_by_len[i] = []
    for segment in segments:
        segments_by_len[len(segment)].append(segment)

    segment_map = dict()
    for l in 'abcdefg':
        segment_map[l] = ''

    segments_by_digit[1] = segments_by_len[2].pop()
    segments_by_digit[7] = segments_by_len[3].pop()
    segments_by_digit[4] = segments_by_len[4].pop()
    segments_by_digit[8] = segments_by_len[7].pop()

    segment_map['a'] = subtract_string(segments_by_digit[7], segments_by_digit[1])

    for digits in segments_by_len[6]:
        guess = subtract_strings(digits, [segments_by_digit[1], segments_by_digit[7], segments_by_digit[4]])
        if len(guess) == 1:
            segment_map['g'] = guess
            segments_by_digit[9] = digits
            segments_by_len[6].remove(digits)
            break

    segment_map['e'] = subtract_string(segments_by_digit[8], segments_by_digit[9])

    for digits in segments_by_len[6]:
        guess = subtract_strings(digits, [segments_by_digit[7], segment_map['g'], segment_map['e']])
        if len(guess) == 1:
            segments_by_digit[0] = digits
            segment_map['b'] = guess
            segments_by_len[6].remove(digits)
            break

    segments_by_digit[6] = segments_by_len[6].pop()

    segment_map['c'] = subtract_string(segments_by_digit[0], segments_by_digit[6])
    segment_map['d'] = subtract_string(segments_by_digit[8], segments_by_digit[0])

    for digits in segments_by_len[5]:
        guess = subtract_string(digits, segments_by_digit[6])
        if len(guess) == 0:
            segments_by_digit[5] = digits
            segments_by_len[5].remove(digits)
            break

    for digits in segments_by_len[5]:
        guess = subtract_string(digits, segments_by_digit[5])
        if len(guess) == 2:
            segments_by_digit[2] = digits
            segments_by_len[5].remove(digits)
            break

    segments_by_digit[3] = segments_by_len[5].pop()
    segment_map['f'] = subtract_strings(segments_by_digit[8], [segments_by_digit[2], segment_map['b']])

    return segments_by_digit


def part_one(in_file_name):
    in_file = open(in_file_name)

    counts = [0] * 10

    for line in in_file:
        [segments, output] = [e.strip() for e in line.split('|')]
        segments = segments.split(' ')
        segments.sort(key=len_key)
        output = output.split(' ')

        segments_by_digit = build_segments_by_digit(segments)

        for output_string in output:
            for key in segments_by_digit.keys():
                digit_segments = segments_by_digit[key]
                if are_strings_equal(output_string, digit_segments):
                    counts[key] += 1
                    break

    print(counts[1] + counts[4] + counts[7] + counts[8])


def part_two(in_file_name):
    in_file = open(in_file_name)

    num_sum = 0

    for line in in_file:
        [segments, output] = [e.strip() for e in line.split('|')]
        segments = segments.split(' ')
        segments.sort(key=len_key)
        output = output.split(' ')

        segments_by_digit = build_segments_by_digit(segments)

        number = 0

        for output_stringi, output_string in enumerate(output):
            for key in segments_by_digit.keys():
                digit_segments = segments_by_digit[key]
                if are_strings_equal(output_string, digit_segments):
                    number += key * (10 ** (3 - output_stringi))
                    break

        num_sum += number

    print(num_sum)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Puzzle 08')
    parser.add_argument('--part', choices=['one', 'two'], required=True)
    parser.add_argument('in_file')
    args = parser.parse_args()

    match args.part:
        case 'one':
            part_one(args.in_file)
        case 'two':
            part_two(args.in_file)
