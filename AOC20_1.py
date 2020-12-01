from helpers import file_reader
from itertools import combinations
import math


def compute(data, entries):
    clean_data = [int(x) for x in data]
    unique_combos = combinations(clean_data, entries)
    for combo in unique_combos:
        if sum(combo) == 2020:
            return math.prod(combo)
    return None


if __name__ == '__main__':
    t0_raw = """1721
    979
    366
    299
    675
    1456
    """
    t0 = [x.strip() for x in t0_raw.strip().split('\n')]
    assert compute(t0, 2) == 514579
    assert compute(t0, 3) == 241861950

    day1 = file_reader('2020_1', output='lines')
    print("solution part 1:", compute(day1, 2))
    print("solution part 2:", compute(day1, 3))
