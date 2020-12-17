import numpy as np
from typing import List, Tuple
from time import perf_counter

"""
Description:
During a cycle, all cubes simultaneously change their state according to the following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
    Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
    Otherwise, the cube remains inactive.

Algorithm steps:
    1) calculate grid size
    2) create empty grid of that size
    3) populate grid with starting position
    4) check if active count is correct
    5) run cycles
        every cycle:
        a) initialize make_passive and make_active lists
        then for each cell:
        a) get neighbours slice, which is 27 cells including self (81 in part 2)
        a) count how many of these 27 (or 81) cells are active
        b) check if cell itself is passive or active
        c) if active subtract 1 from count (self)
        d) if cell is active and count not in {2, 3} add cell to make_passive
        d) if cell is passive and count == 3 add cell to make_active    
    6) modify all cells in make_passive to '.'
    7) modify all cells in make_active to '#'
"""


def grid_size(initial_size: int, cycles: int) -> Tuple:
    f = 1 + (cycles * 2)
    r = c = initial_size + (cycles * 2)
    return f, r, c


def grid_size_4d(initial_size: int, cycles: int) -> Tuple:
    z = 1 + (cycles * 2)
    f = r = c = initial_size + (cycles * 2)
    return z, f, r, c


def get_slice(location: Tuple) -> List[Tuple[int, int]]:
    grid_slice: List[Tuple[int, int]] = []
    for loc in location:
        left = max(loc - 1, 0)
        right = loc + 2
        grid_slice.append((left, right))
    return grid_slice


def initial_grid(data: str) -> List[List[str]]:
    initial = []
    for line in data.strip().split("\n"):
        row = [x for x in line]
        initial.append(row)
    return initial


def create_grid(data: List, cycles: int):
    f, r, c = grid_size(len(data), cycles)
    empty = [[["." for _ in range(c)] for _ in range(r)] for _ in range(f)]
    grid = np.array(empty)
    start_floor = len(grid) // 2
    start_row = start_col = start_floor
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == "#":
                grid[start_floor, start_row + row, start_col + col] = "#"
    return grid


def create_grid_4d(data: List, cycles: int):
    z, f, r, c = grid_size_4d(len(data), cycles)
    empty = [
        [[["." for _ in range(c)] for _ in range(r)] for _ in range(f)]
        for _ in range(z)
    ]
    grid = np.array(empty)
    start_zap = len(grid) // 2
    start_floor = start_row = start_col = start_zap
    for row in range(len(data[0])):
        for col in range(len(data[0])):
            if data[row][col] == "#":
                grid[start_zap, start_floor, start_row + row, start_col + col] = "#"
    return grid


def compute(data: str, cycles=6) -> int:
    """
    Return number of active cubes after all cycles have run.
    Solution part 1.
    """
    initial = initial_grid(data)
    grid = create_grid(initial, cycles)
    height = len(grid)
    depth = width = len(grid[0])
    for c in range(cycles):
        make_passive = []
        make_active = []
        for floor in range(height):
            for row in range(depth):
                for col in range(width):
                    (a, b), (c, d), (e, f) = get_slice((floor, row, col))
                    count = np.count_nonzero(grid[a:b, c:d, e:f] == "#")
                    if grid[floor, row, col] == "#":
                        if count - 1 not in {2, 3}:
                            make_passive.append((floor, row, col))
                    elif grid[floor, row, col] == ".":
                        if count == 3:
                            make_active.append((floor, row, col))
        for pas in make_passive:
            f, r, c = pas
            grid[f, r, c] = "."
        for act in make_active:
            f, r, c = act
            grid[f, r, c] = "#"
    return np.count_nonzero(grid == "#")


def compute_two(data: str, cycles=6) -> int:
    """
    Return number of active cubes after all cycles have run.
    Solution part 2.
    """
    initial = initial_grid(data)
    grid = create_grid_4d(initial, cycles)
    zappers = len(grid)
    height = depth = width = len(grid[0])
    for c in range(cycles):
        make_passive = []
        make_active = []
        # TODO: refactor, as not all floors need to be checked for first n-1 rounds
        for zap in range(zappers):
            for floor in range(height):
                for row in range(depth):
                    for col in range(width):
                        (a, b), (c, d), (e, f), (g, h) = get_slice(
                            (zap, floor, row, col)
                        )
                        count = np.count_nonzero(grid[a:b, c:d, e:f, g:h] == "#")
                        cell = grid[zap, floor, row, col]
                        if cell == "#":
                            if count - 1 not in {2, 3}:
                                make_passive.append((zap, floor, row, col))
                        elif cell == ".":
                            if count == 3:
                                make_active.append((zap, floor, row, col))
        for pas in make_passive:
            z, f, r, c = pas
            grid[z, f, r, c] = "."
        for act in make_active:
            z, f, r, c = act
            grid[z, f, r, c] = "#"
    return np.count_nonzero(grid == "#")


t0 = """
.#.
..#
###
"""

day17 = """
.##...#.
.#.###..
..##.#.#
##...#.#
#..#...#
#..###..
.##.####
..#####.
"""

if __name__ == "__main__":
    print("calculating...")
    assert compute(t0) == 112
    assert compute_two(t0) == 848
    st = perf_counter()
    p1 = compute(day17)
    p2 = compute_two(day17)
    end = perf_counter()
    print(f"solution part 1: {p1}")
    print(f"solution part 2: {p2}")
    print(f"runtime: {round((end - st), 1)}secs")
