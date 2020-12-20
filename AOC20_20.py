from collections import defaultdict
import numpy as np
import math
from helpers import file_reader
from typing import Dict, List
from pprint import pprint


def get_sides_dict(data: List[str]) -> Dict:
    """
    Return dictionary of sets.
        Keys -> tile names
        Values -> sides
    """
    sides_dict = {}
    for square in data:
        lines = [line.strip() for line in square.split("\n")]
        raw_title = lines[0]
        title = raw_title[5:-1]
        tile = np.array([list(line) for line in lines[1:]])
        top = tile[0, :]
        bottom = tile[-1, :]
        left = tile[:, 0]
        right = tile[:, -1]
        sides = [top, bottom, left, right]
        possible_sides = set()
        for side in sides:
            possible_sides.add("".join(side))
            possible_sides.add("".join(side[::-1]))
        sides_dict[title] = possible_sides
    return sides_dict


def compute(data: str) -> int:
    """
    Find corner tiles and return the product of their IDs.
    Solution part 1.
    """
    raw_tiles = [t.strip() for t in data.strip().split("\n\n")]
    sides_dict = get_sides_dict(raw_tiles)
    all_sides = set()
    for tile in sides_dict.values():
        all_sides |= tile
    side_matches = defaultdict(list)
    for side in all_sides:
        for key, cube_sides in sides_dict.items():
            if side in cube_sides:
                side_matches[side].append(key)
    match_table = defaultdict(set)
    for match in side_matches.values():
        if len(match) > 1:
            left, right = match
            match_table[left].add(right)
            match_table[right].add(left)
    corners = []
    for name, pair in match_table.items():
        if len(pair) == 2:
            corners.append(int(name))
    return math.prod(corners)


if __name__ == "__main__":
    t0 = file_reader("AOC20_20_testinput.txt")
    assert compute(t0) == 20899048083289
    day20 = file_reader("inputs/2020_20.txt")
    p1 = compute(day20)
    print(f"solution part 1: {p1}")
