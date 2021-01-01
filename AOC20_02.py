from typing import List, NamedTuple
from time import perf_counter

TRANSLATE_TABLE = {ord(k): v for k, v in {"-": ",", " ": ",", ":": ""}.items()}


class Password(NamedTuple):
    low: int
    high: int
    char: str
    content: str


def translate(password: str) -> Password:
    """Parse string and return as Passwords (=NamedTuple)"""
    password_data = password.translate(TRANSLATE_TABLE)
    mini, maxi, char, name = password_data.split(",")
    return Password(int(mini), int(maxi), char, name)


def get_input(data_file) -> List[Password]:
    """Read data file and return as list of Passwords."""
    with open(data_file) as f:
        return [translate(x.strip()) for x in f.readlines()]


def compute_p1(data: List[Password]) -> int:
    """
    Return number of passwords that comply with policy described
    in part one.
    """
    valid = 0
    for pw in data:
        char_count = pw.content.count(pw.char)
        if pw.low <= char_count <= pw.high:
            valid += 1
    return valid


def compute_p2(data: List[Password]) -> int:
    """
    Return number of passwords that comply with policy described
    in part two.
    """
    valid = 0
    for pw in data:
        # subtract 1 from low/high to account for 1-indexing
        left_match = pw.content[pw.low - 1] == pw.char
        right_match = pw.content[pw.high - 1] == pw.char
        if left_match ^ right_match:  # Exclusive OR (XOR) as need ONE match
            valid += 1
    return valid


if __name__ == "__main__":
    t0 = "1-3 a: abcde"  # True, True
    t1 = "1-3 b: cdefg"  # False, False
    t2 = "2-9 c: ccccccccc"  # True, False
    t3 = "7-15 w: wwwwwcqwwwwwwwww"  # True, True
    t4 = "13-14 s: wznksvkfvfskfs"  # False, True

    test_cases = [translate(x) for x in [t0, t1, t2, t3, t4]]
    assert compute_p1(test_cases) == 3
    assert compute_p2(test_cases) == 3

    start = perf_counter()
    day2 = get_input("inputs/2020_2.txt")

    sp1 = perf_counter()
    p1 = compute_p1(day2)
    sp2 = perf_counter()
    p2 = compute_p2(day2)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms")
