from typing import List
from time import perf_counter


def get_input(data_file: str) -> List[int]:
    with open(data_file) as f:
        return [int(x) for x in f.readlines()]


def compute_p1(data: List[int]) -> int:
    """
    Count the 1 and 3 jolt differences and return their product.
    Solution part one.
    """
    all_adapters = sorted(data)
    device = all_adapters[-1] + 3
    all_adapters.append(device)
    cur_jolts = 0
    jolt_differences = []
    for adapter in all_adapters:
        differences = adapter - cur_jolts
        jolt_differences.append(differences)
        cur_jolts = adapter
    ones = jolt_differences.count(1)
    threes = jolt_differences.count(3)
    return ones * threes


def compute_p2(data: List[int]) -> int:
    """
    Return the total number of distinct ways you can arrange the adapters
    to connect the charging outlet to your device. Uses a dynamic programming
    algorithm. Solution part two.
    """
    arrangements = {}
    all_adapters = [0] + sorted(data)
    arrangements[all_adapters[0]] = 1
    arrangements[all_adapters[1]] = 1
    for i, adapter in enumerate(all_adapters[2:], start=2):
        previous = all_adapters[max(i - 3, 0): i]
        sources = 0
        for p in previous:
            if adapter - p < 4:
                sources += arrangements[p]
        arrangements[adapter] = sources
    return arrangements[all_adapters[-1]]


if __name__ == "__main__":
    t0 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    t1 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
          38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]

    assert compute_p1(t0) == 35
    assert compute_p1(t1) == 220
    assert compute_p2(t0) == 8
    assert compute_p2(t1) == 19208

    start = perf_counter()
    day10 = get_input("inputs/2020_10.txt")
    sp1 = perf_counter()
    p1 = compute_p1(day10)
    sp2 = perf_counter()
    p2 = compute_p2(day10)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
