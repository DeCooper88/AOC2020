from helpers import file_reader
from itertools import combinations

t0_raw = """1721
979
366
299
675
1456
"""

t0 = [x.strip() for x in t0_raw.strip().split('\n')]
# print(t0)


def compute(data):
    clean = [int(x) for x in data]
    combos = combinations(clean, 3)
    for combo in combos:
        left, mid, right = combo
        if left + right + mid == 2020:
            return left * right * mid
    return False


def compute_two(data):
    pass

# print(compute(t0))

day_raw = file_reader('2020_1', output='lines')
# print(day_raw)

print(compute(day_raw))

