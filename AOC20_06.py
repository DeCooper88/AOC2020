from typing import List
from time import perf_counter


def get_input(data_file: str) -> List[List[str]]:
    """Import data and clean data."""
    with open(data_file) as f:
        groups = [x.strip() for x in f.read().split("\n\n")]
        return [x.split("\n") for x in groups]


def compute_p1(data: List[List[str]]) -> int:
    """
    For each group, count the number of questions to which ANYONE answered
    "yes" (set unions). Return the sum of those counts.
    """
    anyone_yes = 0
    for group in data:
        any_yes = set()
        for person in group:
            any_yes |= set(person)
        anyone_yes += len(any_yes)
    return anyone_yes


def compute_p2(data: List[List[str]]) -> int:
    """
    For each group, count the number of questions to which EVERYONE answered
    "yes" (set intersections). Return the sum of those counts.
    """
    everyone_yes = 0
    for group in data:
        all_yes = set(group[0])
        for person in group[1:]:
            all_yes &= set(person)
        everyone_yes += len(all_yes)
    return everyone_yes


if __name__ == "__main__":
    t0 = [["abc"], ["a", "b", "c"], ["ab", "ac"], ["a", "a", "a", "a"], ["b"]]
    assert compute_p1(t0) == 11
    assert compute_p2(t0) == 6

    start = perf_counter()
    day6 = get_input("inputs/2020_6.txt")
    sp1 = perf_counter()
    p1 = compute_p1(day6)
    sp2 = perf_counter()
    p2 = compute_p2(day6)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"Solution part 1: {p1} ({time1}ms)")
    print(f"Solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
