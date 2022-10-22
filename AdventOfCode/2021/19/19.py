from io import FileIO
from os import stat
import sys
import argparse
from math import cos, floor, ceil, pi, radians, sin, sqrt

from dataclasses import dataclass
from functools import reduce
from enum import Enum, auto

import re
from typing import TextIO
from multiprocessing import Pool

INFINITY = 9223372036854775805

sys.path.append("../../../")
from util.term_control import (
    TermControl,
    TermColor,
)  # pylint: disable=wrong-import-position,import-error


class Vec3:
    """
    Represents a two dimensional vector.
    """

    x: int
    y: int
    z: int

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def clone(self) -> "Vec3":
        """Create a new copy of the vector."""
        return Vec3(self.x, self.y, self.z)

    def remap(self, remap: str) -> "Vec3":
        """Returns a new vector where coordinates have been remapped with remap."""
        new_vec = self.clone()

        match remap[1]:
            case "x":
                new_vec.x = self.x
            case "y":
                new_vec.x = self.y
            case "z":
                new_vec.x = self.z

        match remap[0]:
            case "-":
                new_vec.x = -new_vec.x

        match remap[3]:
            case "x":
                new_vec.y = self.x
            case "y":
                new_vec.y = self.y
            case "z":
                new_vec.y = self.z

        match remap[2]:
            case "-":
                new_vec.y = -new_vec.y

        match remap[5]:
            case "x":
                new_vec.z = self.x
            case "y":
                new_vec.z = self.y
            case "z":
                new_vec.z = self.z

        match remap[4]:
            case "-":
                new_vec.z = -new_vec.z

        return new_vec

    def subtract(self, other: "Vec3"):
        """Returns a new vector with result of `self - other`."""
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def add(self, other: "Vec3"):
        """Returns a new vector with result of `self + other`."""
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def equal(self, other: "Vec3"):
        """Returns true if vectors are equal."""
        return self.x == other.x and self.y == other.y and self.z == other.z

    def distance_to(self, other: "Vec3"):
        """Returns distance between vectors."""
        return sqrt(
            pow(other.x - self.x, 2)
            + pow(other.y - self.y, 2)
            + pow(other.z - self.z, 2)
        )

    def __eq__(self, other: "Vec3"):
        return self.equal(other)

    def manhattan_distance(self, other: "Vec3"):
        """Calculates Manhattan distance between two vectors."""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Vec3Map:
    """
    Represents a vector map.
    """

    vectors: list[Vec3]
    origin: Vec3
    aligned: bool

    def __init__(self):
        self.vectors = []
        self.origin = Vec3(0, 0, 0)
        self.aligned = False

    def append(self, vec: Vec3):
        """Appends vector to end of vector map."""
        self.vectors.append(vec)

    def remap(self, remap: str) -> "Vec3Map":
        """Creates a new vector map with `remap` applied to all vectors."""
        new_map = self.clone()
        for (i, _) in enumerate(new_map.vectors):
            new_map.vectors[i] = new_map.vectors[i].remap(remap)
        new_map.origin = new_map.origin.remap(remap)
        return new_map

    def clone(self) -> "Vec3Map":
        """Creates a new copy of the vector map."""
        new_map = Vec3Map()
        for vec in self.vectors:
            new_map.append(vec.clone())
        new_map.origin = self.origin.clone()
        return new_map

    def translate(self, translation: Vec3) -> "Vec3Map":
        """Creates a new copy of the vector map with all vectors translated by `translation`."""
        new_map = self.clone()
        for (i, _) in enumerate(new_map.vectors):
            new_map.vectors[i] = new_map.vectors[i].add(translation)
        new_map.origin = new_map.origin.add(translation)
        return new_map

    def match_points(self, other: "Vec3Map"):
        """Returns a number of vectors that have an equal vector in `other`."""
        self_vectors = self.vectors.copy()
        other_vectors = other.vectors.copy()
        matches = 0

        while True:
            found_match = False

            for self_v in self_vectors:
                for other_v in other_vectors:
                    if self_v.equal(other_v):
                        matches += 1
                        self_vectors.remove(self_v)
                        other_vectors.remove(other_v)
                        found_match = True
                        break
                if found_match:
                    break

            if not found_match:
                break

        return matches

    def __str__(self):
        result = ""
        for vec in self.vectors:
            result += f"{vec}\n"
        return result


def make_remaps():
    """Creates a list of 2d remaps."""
    remaps = []  # xyz

    for coords in ["xyz", "yxz", "zxy"]:
        for signs in ["+++", "++-", "+-+", "+--", "-++", "-+-", "--+", "---"]:
            remap = ""
            for i in range(2):
                remap = remap + f"{signs[i]}{coords[i]}"
            remaps.append(remap)

    return remaps


class Matrix:
    """A mathematical matrix."""

    values: list[int]
    width: int
    height: int

    @staticmethod
    def make(width: int, height: int, val: int = 0) -> "Matrix":
        values = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(val)
            values.append(row)
        return Matrix(values)

    @staticmethod
    def from_vector(vec: Vec3) -> "Matrix":
        return Matrix([[vec.x], [vec.y], [vec.z]])

    def to_vector(self) -> Vec3:
        if not (self.height == 3 and self.width == 1):
            assert False, "Converting incompatible matrix to vector"
        return Vec3(
            round(self.values[0][0]), round(self.values[1][0]), round(self.values[2][0])
        )

    def __init__(self, values: list[list[int]]):
        self.values = values
        self.width = len(values[0])
        self.height = len(values)

    def print(self):
        for row in self.values:
            for col in row:
                print(f"{col} ", end="")
            print()
        print()

    def multiply(self, other: "Matrix"):
        if self.width != other.height:
            assert False, "Multiplying matrices of incompatible sizes"

        sz = self.width

        result = []
        for i in range(self.height):
            row = []
            for j in range(other.width):
                cell_result = 0
                for s in range(sz):
                    cell_result += self.values[i][s] * other.values[s][j]
                row.append(cell_result)
            result.append(row)

        return Matrix(result)


def print_matrices():
    for axis in "xyz":
        for degrees in [radians(0), radians(90), radians(180), radians(270)]:
            print(round(sin(degrees)))


def rx(x: float, v: Vec3) -> Vec3:
    mata = Matrix([[1, 0, 0], [0, cos(x), -sin(x)], [0, sin(x), cos(x)]])
    matb = Matrix.from_vector(v)

    return mata.multiply(matb).to_vector()


def ry(x: float, v: Vec3) -> Vec3:
    mata = Matrix([[cos(x), 0, sin(x)], [0, 1, 0], [-sin(x), 0, cos(x)]])
    matb = Matrix.from_vector(v)

    return mata.multiply(matb).to_vector()


def rz(x: float, v: Vec3) -> Vec3:
    mata = Matrix([[cos(x), -sin(x), 0], [sin(x), cos(x), 0], [0, 0, 1]])
    matb = Matrix.from_vector(v)

    return mata.multiply(matb).to_vector()


def vec_to_remap(vec: Vec3):
    result = ""
    for a in [vec.x, vec.y, vec.z]:
        sign = "+" if a > 0 else "-"
        letter = ""
        match abs(a):
            case 1:
                letter = "x"
            case 2:
                letter = "y"
            case 3:
                letter = "z"
        result += f"{sign}{letter}"
    return result


def generate_remaps():
    remaps = []

    # facing +x
    a = Vec3(1, 2, 3)
    remaps.append(vec_to_remap(a))

    a = rx(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(90), a)

    # facing +z
    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))

    a = rz(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(90), a)

    # facing -x
    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))

    a = rx(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rx(radians(-90), a)

    # facing -z
    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))

    a = rz(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = rz(radians(-90), a)

    # facing +y
    a = ry(radians(-90), a)
    a = rz(radians(90), a)
    remaps.append(vec_to_remap(a))

    a = ry(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(90), a)

    # facing -y
    a = rx(radians(180), a)
    remaps.append(vec_to_remap(a))

    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(-90), a)
    remaps.append(vec_to_remap(a))
    a = ry(radians(-90), a)

    return remaps


def align_vectors(unaligned: Vec3Map, aligned: Vec3Map, remaps: list[str]) -> Vec3Map:
    for remap in remaps:
        vecsb = unaligned.remap(remap)
        for vecb in vecsb.vectors:
            for veca in aligned.vectors:
                translation = veca.subtract(vecb)
                tvecsb = vecsb.translate(translation)
                matches = aligned.match_points(tvecsb)
                if matches == 12:
                    tvecsb.aligned = True
                    return tvecsb

    return None


def align_scanners(scanners: list[Vec3Map]):
    remaps = generate_remaps()

    scanners[0].aligned = True
    left_unaligned = len(scanners) - 1

    with Pool(8) as p:
        while left_unaligned > 0:
            found = False
            for unalignedi in range(len(scanners)):
                if scanners[unalignedi].aligned:
                    continue
                print(f"Aligning {unalignedi}")
                tasks = []
                for alignedi in range(len(scanners)):
                    if not scanners[alignedi].aligned:
                        continue
                    print(f"  with {alignedi}")
                    tasks.append(
                        p.apply_async(
                            align_vectors,
                            [scanners[unalignedi], scanners[alignedi], remaps],
                        )
                    )

                results = [res.get() for res in tasks]
                results = [res for res in results if res]
                if len(results) > 0:
                    newly_aligned = results[0]
                    scanners[unalignedi] = newly_aligned
                    found = True
                    print(f"    aligned")
                    break
            if found:
                left_unaligned -= 1
                print(f"Left unaligned {left_unaligned}")
                print()


def read_scanners(in_file: TextIO):
    scanners: list[Vec3Map] = []

    while _ := in_file.readline().strip():
        scanner = Vec3Map()
        while coords_line := in_file.readline().strip():
            coords = [int(x) for x in coords_line.split(",")]
            scanner.append(Vec3(coords[0], coords[1], coords[2]))
        scanners.append(scanner)

    return scanners


def part_one(in_file: TextIO, out_file: TextIO):
    scanners = read_scanners(in_file)

    align_scanners(scanners)

    all_vecs = []
    for scanner in scanners:
        all_vecs += scanner.vectors

    unique_vecs = []
    for vec in all_vecs:
        if vec not in unique_vecs:
            unique_vecs.append(vec)

    print(f"Number of beacons: {len(unique_vecs)}")
    out_file.write(str(len(unique_vecs)))


def part_two(in_file: TextIO, out_file: TextIO):
    scanners = read_scanners(in_file)

    align_scanners(scanners)

    max_distance = 0
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            distance = scanners[i].origin.manhattan_distance(scanners[j].origin)
            if distance > max_distance:
                max_distance = distance

    print(f"Longest distance: {max_distance}")
    out_file.write(str(max_distance))


def main(file_name, part):
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
