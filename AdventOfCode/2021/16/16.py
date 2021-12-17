from os import stat
import sys
import argparse

from dataclasses import dataclass
from functools import reduce
from enum import Enum

INFINITY = 9223372036854775805

sys.path.append('../../../')
from util.term_control import TermControl, TermColor  # pylint: disable=wrong-import-position,import-error


hex_to_bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


class BitStream:
    def __init__(self):
        self.data = ''

    @staticmethod
    def from_hex_data(hex_data: str) -> 'BitStream':
        stream = BitStream()
        for h in hex_data:
            stream.data += hex_to_bin[h]
        return stream

    @staticmethod
    def from_bin_data(bin_data: str) -> 'BitStream':
        stream = BitStream()
        stream.data = bin_data
        return stream

    def take_int(self, count):
        return int(self.take(count), 2)

    def take(self, count):
        result = self.data[:count]
        self.data = self.data[count:]
        return result

    def __len__(self):
        return len(self.data)


class Packet:
    version: int
    type_id: int
    sub_packets: list['Packet']
    value: int
    length_type_id: int

    def __init__(self):
        self.version = None
        self.type_id = None
        self.sub_packets = []
        self.value = None

    def __str__(self):
        packets_str = '[' + ', '.join([str(packet) for packet in self.sub_packets]) + ']'
        return f'Packet(version={self.version}, type_id={self.type_id}, value={self.value}, packets={packets_str})'


def read_literal(stream: BitStream):
    bits_read = 0
    reading = True
    literal_bits = ''
    while reading:
        bits_read += 5
        bits = stream.take(5)
        reading = bits[0] == '1'
        literal_bits += bits[1:]

    return int(literal_bits, 2)


def read_packet(stream: BitStream) -> Packet:
    packet = Packet()

    packet.version = stream.take_int(3)
    packet.type_id = stream.take_int(3)

    match packet.type_id:
        case 4:
            packet.value = read_literal(stream)
        case _:
            packet.length_type_id = stream.take_int(1)
            match packet.length_type_id:
                case 0:
                    bit_run_length = stream.take_int(15)
                    run_stream = BitStream.from_bin_data(stream.take(bit_run_length))
                    while len(run_stream) > 0:
                        packet.sub_packets.append(read_packet(run_stream))
                case 1:
                    packet_count = stream.take_int(11)
                    for i in range(packet_count):
                        packet.sub_packets.append(read_packet(stream))

    return packet


def count_versions(packet: Packet) -> int:
    sum = packet.version
    for sub_packet in packet.sub_packets:
        sum += count_versions(sub_packet)
    return sum


def part_one(in_file, out_file):
    with open(in_file_name, 'r', encoding='utf-8') as in_file:
        hex_data = in_file.readline().strip()
        stream = BitStream.from_hex_data(hex_data)
        packet = read_packet(stream)
        out_file.write(str(count_versions(packet)))


def evaluate_sub_packets(sub_packets: list[Packet]):
    return [evaluate_expression(sub_packet) for sub_packet in sub_packets]


def evaluate_expression(packet: Packet) -> int:
    match packet.type_id:
        case 4:  # literal
            return packet.value
        case 0:  # sum
            return sum(evaluate_sub_packets(packet.sub_packets))
        case 1:  # product
            return reduce(lambda a, b: a * b, evaluate_sub_packets(packet.sub_packets), 1)
        case 2:  # min
            return min(evaluate_sub_packets(packet.sub_packets))
        case 3:  # max
            return max(evaluate_sub_packets(packet.sub_packets))
        case 5:  # greater-than
            values = evaluate_sub_packets(packet.sub_packets)
            return 1 if values[0] > values[1] else 0
        case 6:  # less-than
            values = evaluate_sub_packets(packet.sub_packets)
            return 1 if values[0] < values[1] else 0
        case 7:  # equal-to
            values = evaluate_sub_packets(packet.sub_packets)
            return 1 if values[0] == values[1] else 0


def part_two(in_file, out_file):
    hex_data = in_file.readline().strip()
    stream = BitStream.from_hex_data(hex_data)
    packet = read_packet(stream)
    out_file.write(str(evaluate_expression(packet)))


def main(in_file, part):
    with open(f'{in_file}.in', 'r', encoding='utf-8') as in_file:
        with open(f'{in_file}.{part}.out', 'w', encoding='utf-8') as out_file:
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
