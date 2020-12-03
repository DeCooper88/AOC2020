import itertools
import math
from helpers import file_reader
from time import perf_counter


def compute(data, entries):
    unique_combinations = itertools.combinations(data, entries)
    for combination in unique_combinations:
        if sum(combination) == 2020:
            return math.prod(combination)
    return None


if __name__ == "__main__":
    t0_raw = "1721 979 366 299 675 1456"
    t0 = [int(x.strip()) for x in t0_raw.strip().split(" ")]
    # test part 1
    assert compute(t0, 2) == 514579
    # test part 2
    assert compute(t0, 3) == 241861950

    day1_raw = file_reader("inputs/2020_1.txt", output="lines")
    day1 = [int(x) for x in day1_raw]
    start = perf_counter()
    p1 = compute(day1, 2)
    middle = perf_counter()
    p2 = compute(day1, 3)
    end = perf_counter()
    t1 = int((middle - start) * 1000)
    t2 = int((end - middle) * 1000)
    print(f"solution part 1: {p1} ({t1}ms)")
    print(f"solution part 2: {p2} ({t2}ms)")
