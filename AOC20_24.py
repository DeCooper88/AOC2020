from helpers import file_reader
from typing import List, Set, Tuple
from time import perf_counter

MOVES = {
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


def find_target(instruction: str) -> Tuple[int, int]:
    """
    Follow navigation instructions and return locsation found.
    Helper function part 1.
    """
    instruction_length = len(instruction)
    pointer = 0
    location = (0, 0)
    while pointer < instruction_length:
        if instruction[pointer] in {"e", "w"}:
            inst = instruction[pointer]
            pointer_adjustment = 1
        else:
            inst = instruction[pointer : pointer + 2]
            pointer_adjustment = 2
        move = MOVES[inst]
        x, y = location
        dx, dy = move
        location = (x + dx, y + dy)
        pointer += pointer_adjustment
    return location


def compute(data: List[str], part_one=True):
    """
    Navigate to tile based on instruction and flip to opposite colour
    (black -> white or white -> black). If part_one is True return number
    of black tiles after all instructions have been executed (solution
    part 1). Otherwise return set with all black tiles (input part 2).
    """
    blacks: Set[Tuple[int, int]] = set()
    for instruction in data:
        target = find_target(instruction)
        if target in blacks:
            blacks.remove(target)
        else:
            blacks.add(target)
    return len(blacks) if part_one else blacks


def neighbours(tile: Tuple) -> Set[Tuple[int, int]]:
    """Return all neighbours for tile."""
    all_neighbours = set()
    x, y = tile
    for move in MOVES.values():
        dx, dy = move
        nb = (x + dx, y + dy)
        all_neighbours.add(nb)
    return all_neighbours


def compute_two(data: List[str], rounds: int) -> int:
    """
    Return number of black tiles after all rounds have been
    processed. Solution for part 2.
    """
    blacks = compute(data, part_one=False)
    for rnd in range(rounds):
        whites = set()
        for b in blacks:
            nbs = neighbours(b)
            not_black = nbs - blacks
            whites |= not_black
        to_white = set()
        for bt in blacks:
            bnbs = neighbours(bt)
            black_neighbours = len(blacks & bnbs)
            if black_neighbours not in {1, 2}:
                to_white.add(bt)
        to_black = set()
        for wt in whites:
            wnbs = neighbours(wt)
            black_neighbours = len(blacks & wnbs)
            if black_neighbours == 2:
                to_black.add(wt)
        blacks = blacks - to_white
        blacks = blacks | to_black
    return len(blacks)


if __name__ == "__main__":
    print("calculating...")

    assert find_target("ee") == (2, 0)
    assert find_target("ww") == (-2, 0)
    assert find_target("nene") == (2, -2)
    assert find_target("neneseseww") == (0, 0)
    assert find_target("seswnwne") == (0, 0)
    assert find_target("eenenewwswsw") == (0, 0)

    t0 = file_reader("examples/AOC20_24_example.txt", output="lines")
    assert compute(t0) == 10
    assert compute_two(t0, 100) == 2208

    start = perf_counter()
    day24 = file_reader("inputs/2020_24.txt", output="lines")
    stp1 = perf_counter()
    p1 = compute(day24)
    stp2 = perf_counter()
    p2 = compute_two(day24, 100)
    end = perf_counter()
    rt_p1 = round((stp2 - stp1) * 1000, 1)
    rt_p2 = round((end - stp2) * 1000, 1)
    total_runtime = round((end - start) * 1000, 1)
    print(f"solution part 1: {p1} ({rt_p1}ms)")
    print(f"solution part 2: {p2} ({rt_p2}ms)")
    print(f"total runtime: {total_runtime}ms")
