from abc import abstractmethod
from typing import Union
from dataclasses import dataclass
import sys
import argparse

from typing import TextIO

# Import libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

INFINITY = 9223372036854775805

sys.path.append("../../../")


def part_one(in_file: TextIO, out_file: TextIO):
    pass


def main(file_name: str, part: str):
    with open(f"{file_name}.in", "r", encoding="utf-8") as in_file:
        with open(f"{file_name}.{part}.out", "w", encoding="utf-8") as out_file:
            match part:
                case "one":
                    part_one(in_file, out_file)
                case "two":
                    part_two(in_file, out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle 16")
    parser.add_argument("--part", choices=["one", "two"], required=True)
    parser.add_argument("in_file")
    args = parser.parse_args()

    main(args.in_file, args.part)
