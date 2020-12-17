import numpy as np
from time import perf_counter


def grid_size(initial_size, cycles):
    f = 1 + (cycles * 2)
    # print("len(data) = ", len(data))
    r = c = initial_size + (cycles * 2)
    return f, r, c


def grid_size_4d(initial_size, cycles):
    z = 1 + (cycles * 2)
    f = r = c = initial_size + (cycles * 2)
    return z, f, r, c


# def full_grid(z, y, x):
#     grid = [[['.' for _ in range(x + 1)] for _ in range(y + 1)] for _ in range(z)]
#     # print(grid)
#     return np.array(grid)


# print(full_grid(3, 5, 5))


def get_slice(location):
    slice = []
    for loc in location:
        left = max(loc - 1, 0)
        right = loc + 2
        slice.append((left, right))
    return slice


def get_slice_4d(location):
    slice = []
    for loc in location:
        left = max(loc - 1, 0)
        right = loc + 2
        slice.append((left, right))
    return slice


# s0 = get_slice((1, 1, 1))
# print(s0)
# (a, b), (c, d), (e, f) = s0
# print(a)
# print(b)


def initial_grid(data):
    initial = []
    for line in data.strip().split('\n'):
        row = [x for x in line]
        initial.append(row)
    return initial


def create_grid(data, cycles):
    f, r, c = grid_size(len(data), cycles)
    empty = [[['.' for _ in range(c)] for _ in range(r)] for _ in range(f)]
    grid = np.array(empty)
    start_floor = len(grid) // 2
    start_row = start_col = start_floor
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == '#':
                grid[start_floor, start_row + row, start_col + col] = '#'
    return grid


def create_grid_4d(data, cycles):
    z, f, r, c = grid_size_4d(len(data), cycles)
    empty = [[[['.' for _ in range(c)] for _ in range(r)] for _ in range(f)] for _ in range(z)]
    grid = np.array(empty)
    start_zap = len(grid) // 2
    start_floor = start_row = start_col = start_zap
    for row in range(len(data[0])):
        for col in range(len(data[0])):
            if data[row][col] == '#':
                grid[start_zap, start_floor, start_row + row, start_col + col] = '#'
    return grid


def compute_two(data, cycles=6):
    # turn initial data into grid
    initial = initial_grid(data)
    # create grid
    grid = create_grid_4d(initial, cycles)
    zappers = len(grid)
    height = depth = width = len(grid[0])
    for c in range(cycles):
        make_passive = []
        make_active = []
        for zap in range(zappers):
            for floor in range(height):
                for row in range(depth):
                    for col in range(width):
                        (a, b), (c, d), (e, f), (g, h) = get_slice_4d((zap, floor, row, col))
                        count = np.count_nonzero(grid[a:b, c:d, e:f, g:h] == '#')
                        cell = grid[zap, floor, row, col]
                        if cell == '#':
                            if count - 1 not in {2, 3}:
                                make_passive.append((zap, floor, row, col))
                        elif cell == '.':
                            if count == 3:
                                make_active.append((zap, floor, row, col))
        # print(len(make_passive))
        # print(make_passive)
        # print(len(make_active))
        # print(make_active)
        for pas in make_passive:
            z, f, r, c = pas
            grid[z, f, r, c] = '.'
        for act in make_active:
            z, f, r, c = act
            grid[z, f, r, c] = '#'
    # print(grid)
    return np.count_nonzero(grid == '#')


def compute(data, cycles=6):
    # turn initial data into grid
    initial = initial_grid(data)
    # create grid
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
                    count = np.count_nonzero(grid[a:b, c:d, e:f] == '#')
                    if grid[floor, row, col] == '#':
                        if count - 1 not in {2, 3}:
                            make_passive.append((floor, row, col))
                    elif grid[floor, row, col] == '.':
                        if count == 3:
                            make_active.append((floor, row, col))
        # print(len(make_passive))
        # print(make_passive)
        # print(len(make_active))
        # print(make_active)
        for pas in make_passive:
            f, r, c = pas
            grid[f, r, c] = '.'
        for act in make_active:
            f, r, c = act
            grid[f, r, c] = '#'
    # print(grid)
    return np.count_nonzero(grid == '#')


"""
During a cycle, all cubes simultaneously change their state according to the following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
    Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
    Otherwise, the cube remains inactive.
    

STEPS:
    1) calculate grid size
    2) create empty grid of that size
    3) populate grid with starting position
    4) check it return correct active count
    5) run cycle
        a) initialize make_passive and make_active lists
        then for each cell
        a) get neighbours slice, which is 27 cells including self
        a) count how many of these 27 cells are active
        b) check if cell itself passive or active
        c) if active subtract 1 from count (self)
        d) if count not in {2, 3} add cell to make_passive
        d) if cell is passive and count == 3 add cell to make_active    
    6) modify all cells in make_passive to '.'
    7) modify all cells in make_active to '#'
"""

t0 = """
.#.
..#
###
"""

t1 = """
.#.
...
..#
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


st = perf_counter()
assert compute(t0, cycles=6) == 112
p1 = compute(day17, cycles=6)
p2 = compute_two(day17, cycles=6)
end = perf_counter()
print(f"solution part 1: {p1}")
print(f"solution part 2: {p2}")
print(f"runtime: {round((end - st), 1)}secs")
