from helpers import file_reader
from itertools import combinations
from typing import List, Union


def compute(data: List[int], preamble: int) -> Union[int, bool]:
    for i in range(preamble, len(data) + 1):
        checksum = data[i]
        nums = data[i - preamble : i]
        all_combos = combinations(nums, 2)
        found_one = False
        for combo in all_combos:
            left, right = combo
            if left == right:
                continue
            if left + right == checksum:
                found_one = True
                break
        if not found_one:
            return checksum
    return False


def compute_two(data: List[int], required: int) -> Union[int, bool]:
    # TODO: check range if not getting result
    for i in range(len(data) + 1):
        sumo = []
        for j in range(i, len(data) + 1):
            sumo.append(data[j])
            if sum(sumo) > required + 1:
                break
            elif sum(sumo) == required:
                return min(sumo) + max(sumo)
    return False


if __name__ == "__main__":
    t0 = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
    ]
    assert compute(t0, 5) == 127
    assert compute_two(t0, 127) == 62

    day9_raw = file_reader("inputs/2020_9.txt", output="lines")
    day9 = [int(x) for x in day9_raw]
    print(compute(day9, 25))
    answer_p1 = 675280050
    print(compute_two(day9, answer_p1))
