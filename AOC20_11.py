from helpers import file_reader
from typing import List, Tuple
import numpy as np
from time import perf_counter


def possible_seats(grid, location, target, rc=False):
    """rc = return count"""
    height = len(grid)
    width = len(grid[0])
    moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
    children = []
    row, col = location
    for move in moves:
        new_row = move[0] + row
        new_col = move[1] + col
        on_grid = 0 <= new_row < height and 0 <= new_col < width
        if not on_grid:
            continue
        is_seat = grid[new_row][new_col] == target
        if is_seat:
            children.append(move)
    return len(children) if rc else children


def find_seats(grid, sign, maximum=10):
    """
    sign can be 'L' for free or '#' for occupied
    maximum is 10 by default, in which case it neighbours is never
    higher than maximum, set value to 4 for rule 2
    """
    seats = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # check if seat is free/occupied
            if grid[row][col] == sign:
                # TODO: refactor, makes function slow
                # if seat is free/occupied find neighbours
                neighbours = possible_seats(grid, (row, col), sign, rc=True)
                if neighbours <= maximum:
                    seats.append((row, col))
    return seats


def modify_seats(grid, locations, new_value):
    for row, col in locations:
        grid[row][col] = new_value
    return grid


def seat_locations(grid):
    seats = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != '.':
                seats.append((row, col))
    return seats


def compute(data, rounds):
    # location = seat_locations(data)
    for i in range(rounds):
        free_seats = find_seats(data, 'L', maximum=4)
        busy_seats = find_seats(data, '#', maximum=4)
        data = modify_seats(data, free_seats, '#')
        print(data)
        data = modify_seats(data, busy_seats, 'L')
    return data


class FloorPlan:
    def __init__(self, grid: List) -> None:
        self.grid = np.array(grid)
        # self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.seats = set()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] != '.':
                    self.seats.add((row, col))
        self.moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1),
                      (1, 1), (1, 0), (1, -1), (0, -1))

    @property
    def occupied(self) -> int:
        seats = 0
        for loc in self.seats:
            row, col = loc
            if self.grid[row][col] == '#':
                seats += 1
        return seats

    def valid_empty_seat(self, location: Tuple) -> bool:
        """
        Return True if seat is free and has no adjacent occupants.
        Checks rule 1.
        """
        row, col = location
        for move in self.moves:
            new_row = move[0] + row
            new_col = move[1] + col
            if (new_row, new_col) not in self.seats:
                continue
            if self.grid[new_row][new_col] == '#':
                return False
        return True

    def too_many_neighbours(self, location: Tuple) -> bool:
        """
        Return True if seat is occupied and has 4 or more occupied
        seats adjacent to it. Checks rule 2.
        """
        row, col = location
        neighbours = 0
        for move in self.moves:
            new_row = move[0] + row
            new_col = move[1] + col
            if (new_row, new_col) not in self.seats:
                continue
            if self.grid[new_row][new_col] == '#':
                neighbours += 1
                if neighbours > 3:
                    return False
        return True

    def locations_rule_one(self) -> List[Tuple]:
        """Return list with all locations that agree with rule one."""
        free_seats = []
        for loc in self.seats:
            if self.valid_empty_seat(loc):
                free_seats.append(loc)
        return free_seats

    def locations_rule_two(self) -> List[Tuple]:
        """Return list with all locations that agree with rule two."""
        busy_seats = []
        for loc in self.seats:
            if not self.too_many_neighbours(loc):
                busy_seats.append(loc)
        return busy_seats

    def apply_changes(self, locations: List[Tuple], new_value) -> None:
        for loc in locations:
            row, col = loc
            self.grid[row][col] = new_value

    def modify(self, rounds: int) -> int:
        for i in range(rounds):
            rule_one_locs = self.locations_rule_one()
            rule_two_locs = self.locations_rule_two()
            print("adjustments needed:", len(rule_one_locs), len(rule_two_locs))
            if len(rule_one_locs) + len(rule_two_locs) == 0:
                return self.occupied
            self.apply_changes(rule_one_locs, '#')
            self.apply_changes(rule_two_locs, 'L')
            print("round", i, "occupied =", self.occupied)

    def __repr__(self):
        floor_plan = ""
        for line in self.grid:
            floor_plan += f"{''.join(line)}\n"
        return floor_plan


t0_raw = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

t1_raw = """
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
"""

t2_raw = """
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
"""

# t0 = np.array([list(x.strip()) for x in t0_raw.strip().split()])
t0_list = [list(x.strip()) for x in t0_raw.strip().split()]
# print(t0)
# t0_locs = seat_locations(t0)
# print(t0_locs)
# print(len(t0_locs))
# print(possible_seats(t0, (1, 1), target='L'))
# print(possible_seats(t0, (1, 1), target='L', rc=True))
# print(possible_seats(t0, (0, 9), target='L'))
# print(possible_seats(t0, (9, 0), target='L'))
# print(possible_seats(t0, (9, 9), target='L'))
# print(possible_seats(t0, (9, 9), target='L', rc=True))

# print(t0)
# print(find_seats(t0, 'L'))
# print(compute(t0, 1))

t0 = FloorPlan(t0_list)
# print(t0)
# print(t0.height)
# print(t0.width)
# print(t0.seats)
# print(t0.moves)
# print(t0.valid_empty_seat((0, 0)))
# print(t0.valid_empty_seat((9, 0)))
# print(t0.too_many_neighbours((0, 0)))
# print(t0.too_many_neighbours((1, 1)))
# print(sorted(t0.locations_rule_two()))


# t0.modify(6)
# print(t0)
# print(t0.occupied)


# t0.modify()
# print(t0)

"""
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
"""




# day11_raw = file_reader('inputs/2020_11.txt', output='lines')
# day11_list = [list(x) for x in day11_raw]
# day11 = FloorPlan(day11_list)
# st = perf_counter()
# day11.modify(100)
# end = perf_counter()
# print()
# print("secs", end - st)


