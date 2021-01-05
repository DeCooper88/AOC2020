from typing import List, Union
from time import perf_counter


def get_input(data_file: str) -> List[int]:
    with open(data_file) as f:
        return [int(x) for x in f.readlines()]


def compute_p1(data: List[int], preamble: int) -> Union[int, bool]:
    """
    Return number for which no sum is found in it's preamble (preamble is
    preceding x numbers). Solution for part one. Input part two.
    """
    selection = set(data[:preamble])
    for i in range(preamble, len(data)):
        target = data[i]
        sum_not_found = True
        for number in selection:
            if target - number in selection:
                sum_not_found = False
        if sum_not_found:
            return target
        drops_off = data[i - preamble]  # value moves outside preamble
        selection.remove(drops_off)  # therefore removed
        selection.add(target)  # target moves inside preamble and added
    return False


def compute_p2(data: List[int], required: int) -> Union[int, bool]:
    """
    Find required contiguous sum and return sum of the min and max of the
    entries tah form this sum. Solution for part two. Algorithm uses
    two-pointers/sliding window technique."""
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
        return min(data[slow : fast + 1]) + max(data[slow : fast + 1])
    return False


def compute_slow(data: List[int], required: int) -> Union[int, bool]:
    """Slow brute force solution for part 2."""
    for i in range(len(data)):
        sumo = []
        for j in range(i, len(data) + 1):
            sumo.append(data[j])
            if sum(sumo) > required:
                break
            elif sum(sumo) == required:
                return min(sumo) + max(sumo)
    return False


def compute_snail(lines: List[int], goal: int) -> Union[int, bool]:
    """
    Solution part two by pro competitive programmer.
    Fast to code, but runs slow.
    """
    for i in range(len(lines)):
        for j in range(i + 2, len(lines)):
            xs = lines[i:j]
            if sum(xs) == goal:
                pp2 = min(xs) + max(xs)
                return pp2
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

    assert compute_p1(t0, 5) == 127
    assert compute_p2(t0, 127) == 62

    start = perf_counter()
    day9 = get_input("inputs/2020_9.txt")
    sp1 = perf_counter()
    p1 = compute_p1(day9, 25)
    sp2 = perf_counter()
    p2 = compute_p2(day9, p1)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
    print("calculating runtime slow solutions...")
    st_slow = perf_counter()
    p2_slow = compute_slow(day9, p1)
    st_snail = perf_counter()
    p2_snail = compute_snail(day9, p1)
    end_slows = perf_counter()
    runtime_slow = round((st_snail - st_slow) * 1000, 1)
    runtime_snail = round((end_slows - st_snail) * 1000, 1)
    assert p2_slow == 96081673
    assert p2_snail == 96081673
    print(f"runtime slow solution: {runtime_slow}ms")
    print(f"runtime snail solution: {runtime_snail}ms")
