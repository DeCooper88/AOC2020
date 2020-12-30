from typing import Callable, Iterable, Set, Union
from time import perf_counter


def get_input(data_file: str) -> Iterable[str]:
    """Yield ticket string by line."""
    with open(data_file) as f:
        return (x.strip() for x in f.readlines())


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
    return (low * 8) + left


def convert_id(boarding_pass: str) -> int:
    """
    Calculate seat ID by translating boarding pass into binary. This function
    follows the instructions and multiplies the row number by 8 before adding
    the seat number. Alternatively you could just convert the full boarding
    pass string to binary, as this would give the same result.
    """
    mapper = {70: "0", 66: "1", 76: "0", 82: "1"}  # maps ord to string
    bin_id = boarding_pass.translate(mapper)
    row = int(bin_id[:7], 2)
    seat = int(bin_id[7:], 2)
    return (row * 8) + seat


def compute_p1(boarding_passes: Iterable[str], converter: Callable) -> Set[int]:
    """
    Return set of all boarding pass IDs. Conversion function can be
    bin_search_id or convert_id. This set is the input for part two. The len
    of this set is the answer for part one.
    """
    return {converter(bp) for bp in boarding_passes}


def compute_p2(seen_seats: Set[int]) -> Union[int, bool]:
    """
    Return seat number that is not in all_boarding_passes. Conversion function
    can be bin_search_id or convert_id. Return False if none or more than 1
    are found.
    """
    all_seats = set(range(min(seen_seats), max(seen_seats)))
    not_seen = all_seats - seen_seats
    return not_seen.pop() if len(not_seen) == 1 else False


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
    assert max(compute_p1(all_tests, bin_search_id)) == 820
    assert max(compute_p1(all_tests, convert_id)) == 820

    start = perf_counter()
    day5 = get_input("inputs/2020_5.txt")
    sp1 = perf_counter()
    all_ticket_ids = compute_p1(day5, convert_id)
    p1 = max(all_ticket_ids)
    sp2 = perf_counter()
    p2 = compute_p2(all_ticket_ids)
    end = perf_counter()

    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 1)
    print(f"Solution part 1: {p1} ({time1}ms)")
    print(f"Solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
