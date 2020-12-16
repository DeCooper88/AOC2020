from typing import List
from time import perf_counter


def compute(data: List[int], target: int) -> int:
    """
    Return last spoken number when turn == target.
    Solution works for both parts, but is slow for part 2.
    """
    seen = {num: i for i, num in enumerate(data[:-1], start=1)}
    spoken = data[-1]
    turn = len(data)
    while True:
        if turn == target:
            return spoken
        if spoken not in seen:
            seen[spoken] = turn
            spoken = 0
        else:
            last_seen = seen[spoken]
            seen[spoken] = turn
            spoken = turn - last_seen
        turn += 1


if __name__ == "__main__":
    assert compute([0, 3, 6], 2020) == 436
    assert compute([1, 3, 2], 2020) == 1
    assert compute([2, 1, 3], 2020) == 10
    assert compute([1, 2, 3], 2020) == 27
    assert compute([2, 3, 1], 2020) == 78
    assert compute([3, 2, 1], 2020) == 438
    assert compute([3, 1, 2], 2020) == 1836

    day15 = [10, 16, 6, 0, 1, 17]
    print("calculating...")
    st = perf_counter()
    p1 = compute(day15, 2020)
    st_p2 = perf_counter()
    p2 = compute(day15, 30000000)
    end = perf_counter()
    t1 = round(st_p2 - st, 2)
    t2 = round(end - st_p2, 2)
    total = round(end - st, 2)
    print(f"solution part 1: {p1}({t1}ms)")
    print(f"solution part 2: {p2}({t2}ms)")
    print(f"runtime: {total} seconds")
