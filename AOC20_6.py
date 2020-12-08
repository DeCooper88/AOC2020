from helpers import file_reader
from collections import Counter
from typing import List
import time


def compute(data: List[List[str]]) -> int:
    count = 0
    for group in data:
        person_count = set()
        for person in group:
            for letter in person:
                person_count.add(letter)
        count += len(person_count)
    return count


def compute_two(data: List[List[str]]) -> int:
    count = 0
    for group in data:
        size_group = len(group)
        q_count = Counter()
        for person in group:
            for letter in person:
                q_count[letter] += 1
        group_count = 0
        for lc in q_count.values():
            if lc == size_group:
                group_count += 1
        count += group_count
    return count


if __name__ == "__main__":
    t0 = [["abc"], ["a", "b", "c"], ["ab", "ac"], ["a", "a", "a", "a"], ["b"]]
    assert compute(t0) == 11
    assert compute_two(t0) == 6

    st = time.perf_counter()
    day6_raw = file_reader("inputs/2020_6.txt")
    day6_groups = [x.strip() for x in day6_raw.split("\n\n")]
    day6 = [x.split("\n") for x in day6_groups]
    p1 = compute(day6)
    p2 = compute_two(day6)
    end = time.perf_counter()
    print(f"solution part 1: {p1}")
    print(f"solution part 2: {p2}")
    print(f"total time: {round((end - st) * 1000, 1)}ms")
