from typing import List
from time import perf_counter


def compute(data: List[int], target: int) -> int:
    """
    Return last spoken number when turn == target.
    Solution works for both parts, but is very slow for part 2.
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


assert compute([0, 3, 6], 2020) == 436
assert compute([1, 3, 2], 2020) == 1
assert compute([2, 1, 3], 2020) == 10
assert compute([1, 2, 3], 2020) == 27
assert compute([2, 3, 1], 2020) == 78
assert compute([3, 2, 1], 2020) == 438
assert compute([3, 1, 2], 2020) == 1836

day15 = [10, 16, 6, 0, 1, 17]
st = perf_counter()
print("solution part 1:", compute(day15, 2020))
end = perf_counter()
print(f"runtime: {round((end - st) * 1000, 1)}ms")
print("Same algorithm will work for part 2, but it will take 90+ seconds")
