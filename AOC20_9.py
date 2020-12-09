from helpers import file_reader
from itertools import combinations
from typing import List, Union
from time import perf_counter


def compute(data: List[int], preamble: int) -> Union[int, bool]:
    """Solution part 1"""
    for i in range(preamble, len(data)):
        checksum = data[i]
        nums = data[i - preamble: i]
        all_combos = combinations(nums, 2)
        sum_not_found = True
        for combo in all_combos:
            left, right = combo
            if left == right:
                continue
            if left + right == checksum:
                sum_not_found = False
                break
        if sum_not_found:
            return checksum
    return False


def compute_fast(data: List[int], required: int) -> Union[int, bool]:
    """Fast two-pointers solution for part 2."""
    slow, fast = 0, 1
    cur_sum = data[slow] + data[fast]
    value_found = False
    while fast != len(data):
        if cur_sum < required:
            fast += 1
            cur_sum += data[fast]
        elif cur_sum > required:
            cur_sum -= data[slow]
            slow += 1
        elif cur_sum == required:
            value_found = True
            break
    if value_found:
        # TODO: remove when done
        # print(slow, fast)
        return min(data[slow: fast + 1]) + max(data[slow: fast + 1])
    return False


def compute_slow(data: List[int], required: int) -> Union[int, bool]:
    """Slow brute force solution for part 2."""
    work_done = 0
    for i in range(len(data)):
        sumo = []
        # sumo = 0
        for j in range(i, len(data) + 1):
            # work_done += 1
            sumo.append(data[j])
            work_done += len(sumo)
            # print(len(sumo))
            # sumo += data[j]
            if sum(sumo) > required:
                break
            elif sum(sumo) == required:
                # print(f"number of items seen: {work_done}")
                return min(sumo) + max(sumo)
                # return min(data[i: j + 1]) + max(data[i: j + 1])
    return False


def compute_snail(lines: List[int], goal: int) -> int:
    """
    Solution by pro competitive programmer for part 2.
    Effective but very slow.
    """
    ops = 0
    for i in range(len(lines)):
        for j in range(i + 2, len(lines)):
            xs = lines[i:j]
            ops += len(xs)
            if sum(xs) == goal:
                pp2 = min(xs) + max(xs)
                # print("number of operations:", ops)
                return pp2


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
    assert compute_fast(t0, 127) == 62

    st = perf_counter()
    day9_raw = file_reader("inputs/2020_9.txt", output="lines")
    day9 = [int(x) for x in day9_raw]
    st1 = perf_counter()
    p1 = compute(day9, 25)
    st2 = perf_counter()
    p2 = compute_fast(day9, p1)
    end = perf_counter()
    p1_time = round((st2 - st1) * 1000, 1)
    p2_time = round((end - st2) * 1000, 1)
    total_time = round((end - st) * 1000, 1)
    print(f"solution part 1: {p1} ({p1_time}ms)")
    print(f"solution part 2: {p2} ({p2_time}ms)")
    print(f"total runtime fast solution, including data import & cleaning {total_time}ms")
    st_slow = perf_counter()
    p2_slow = compute_slow(day9, p1)
    st_snail = perf_counter()
    p2_snail = compute_snail(day9, p1)
    end_slows = perf_counter()
    slow = round((st_snail - st_slow) * 1000, 1)
    snail = round((end_slows - st_snail) * 1000, 1)
    print(f"runtime slow solution {slow}ms")
    print(f"runtime snail solution {snail}ms")
