import itertools
import numpy as np
from typing import Optional, Set
from time import perf_counter


def get_input(data_file: str) -> Set[int]:
    """Read data file and return as set of integers."""
    with open(data_file) as f:
        return {int(x.strip()) for x in f.readlines()}


def compute_one(expenses: Set[int]) -> Optional[int]:
    """
    Find the 2 entries in expenses that add up to 2020 and return
    their product. Solution part one.
    """
    for entry in expenses:
        required = 2020 - entry
        if required in expenses:
            return entry * required
    return None


def compute_two(expenses: Set[int]) -> Optional[int]:
    """
    Find the 3 entries in expenses that add up to 2020 and return
    their product. Solution part two.
    """
    unique_combinations = itertools.combinations(expenses, 2)
    for pair in unique_combinations:
        required = 2020 - sum(pair)
        if required in expenses:
            return np.prod(pair) * required
    return None


if __name__ == "__main__":
    # test part 1
    t0 = {1721, 979, 366, 299, 675, 1456}
    assert compute_one(t0) == 514579
    # test part 2
    assert compute_two(t0) == 241861950

    start = perf_counter()
    day1 = get_input("inputs/2020_1.txt")
    sp1 = perf_counter()
    p1 = compute_one(day1)
    sp2 = perf_counter()
    p2 = compute_two(day1)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total}ms")
