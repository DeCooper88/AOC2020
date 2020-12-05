from helpers import file_reader, translator
from typing import List, Callable
import time


def bin_search_id(boarding_pass: str) -> int:
    """Calculate seat ID using binary search."""
    rows = boarding_pass[:7]
    seats = boarding_pass[7:]
    low, high = 0, 127
    for step in rows:
        if step == "F":  # lower half
            high = (high + low) // 2
        elif step == "B":  # upper half
            low = ((high + low) // 2) + 1
    left, right = 0, 7
    for seat in seats:
        if seat == "L":  # lower half
            right = (left + right) // 2
        elif seat == "R":  # upper half
            left = ((left + right) // 2) + 1
    assert low == high, "row low != row high"
    assert left == right, "seat left != seat right"
    return (low * 8) + left


def convert_id(boarding_pass: str) -> int:
    """Calculate seat ID by translating boarding pass into binary."""
    mapper = {"F": "0", "B": "1", "L": "0", "R": "1"}
    bin_id = translator(boarding_pass, mapper)
    row = int(bin_id[:7], 2)
    seat = int(bin_id[7:], 2)
    return (row * 8) + seat


def compute_one(all_boarding_passes: List[str], conversion_function: Callable) -> int:
    """
    Return boarding pass with highest id in all_boarding_passes.
    Conversion function can be bin_search_id or convert_id.
    """
    return max([conversion_function(bp) for bp in all_boarding_passes])


def compute_two(all_boarding_passes: List[str], conversion_function: Callable) -> int:
    """
    Return seat number that is not in all_boarding_passes and not in front
    or back. Conversion function can be bin_search_id or convert_id.
    """
    seen_seats = {conversion_function(bp) for bp in all_boarding_passes}
    all_seats = set(range(1024))
    not_seen = all_seats - seen_seats
    front = 128
    back = (8 * 128) - 128
    potentials = [seat_id for seat_id in not_seen if front < seat_id < back]
    assert len(potentials) == 1, "More than one seat id found"
    return potentials[0]


if __name__ == "__main__":
    t0 = "FBFBBFFRLR"
    t1 = "BFFFBBFRRR"
    t2 = "FFFBBBFRRR"
    t3 = "BBFFBBFRLL"
    all_tests = [t0, t1, t2, t3]

    assert bin_search_id(t0) == 357
    assert bin_search_id(t1) == 567
    assert convert_id(t2) == 119
    assert convert_id(t3) == 820
    assert compute_one(all_tests, bin_search_id) == 820
    assert compute_one(all_tests, convert_id) == 820

    day5: List[str] = file_reader("inputs/2020_5.txt", output="lines")
    p1_start = time.perf_counter()
    p1m1 = compute_one(day5, bin_search_id)
    p1_middle = time.perf_counter()
    p1m2 = compute_one(day5, convert_id)
    p1_end = time.perf_counter()
    p2m1 = compute_two(day5, bin_search_id)
    p2_middle = time.perf_counter()
    p2m2 = compute_two(day5, convert_id)
    p2_end = time.perf_counter()

    p1t1 = round((p1_middle - p1_start) * 1000, 1)
    p1t2 = round((p1_end - p1_middle) * 1000, 1)
    p2t1 = round((p2_middle - p1_end) * 1000, 1)
    p2t2 = round((p2_end - p2_middle) * 1000, 1)
    print(f"Solution part 1: {p1m1} ({p1t1}ms / {p1t2}ms)")
    print(f"Solution part 2: {p2m1} ({p2t1}ms / {p2t2}ms)")
