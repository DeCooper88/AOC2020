from helpers import file_reader
from typing import List, Tuple, Union
import numpy as np
from time import perf_counter


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

    def visible_neighbours(self, loc: Tuple, move: Tuple) -> Union[str, bool]:
        """
        Return the first seat you see from location in direction of move.
        Should return:
            'L' if empty
            '#' if occupied
            False if none found
        """
        # print("HELLO, you visited visible_neighbours!")
        row, col = loc
        new_row = row + move[0]
        new_col = col + move[1]
        while True:
            if new_row >= self.height or new_row < 0:
                return False
            elif new_col >= self.width or new_col < 0:
                return False
            val = self.grid[new_row][new_col]
            if val == 'L' or val == '#':
                return val
            new_row = new_row + move[0]
            new_col = new_col + move[1]

    def valid_empty_seat(self, location: Tuple) -> bool:
        """
        Return True if seat is free and has no adjacent occupants.
        Checks rule 1 for part 1.
        """
        row, col = location
        # TODO: fixes bug first version 1, test carefully
        if self.grid[row][col] == '#' or self.grid[row][col] == '.':
            return False
        for move in self.moves:
            new_row = move[0] + row
            new_col = move[1] + col
            if (new_row, new_col) not in self.seats:
                continue
            if self.grid[new_row][new_col] == '#':
                return False
        return True

    def valid_empty_seat_two(self, location: Tuple) -> bool:
        """
        Return True if seat is free and has no adjacent occupants.
        Checks rule 1 for part 2.
        """
        row, col = location
        if self.grid[row][col] == '#' or self.grid[row][col] == '.':
            return False
        for move in self.moves:
            new_row = move[0] + row
            new_col = move[1] + col
            if (new_row, new_col) not in self.seats:
                continue
            val = self.visible_neighbours(location, move)
            # print(f"move: {move}  loc: {(new_row, new_col)}  val: {val}")
            if val == '#':
                return False
        return True

    def too_many_neighbours(self, location: Tuple) -> bool:
        """
        Return False if seat is occupied and has 4 or more occupied
        seats adjacent to it. Checks rule 2 for part 1.
        """
        row, col = location
        # TODO: fixes bug first version 1, test carefully
        if self.grid[row][col] != '#':
            return True
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

    def too_many_neighbours_two(self, location: Tuple) -> bool:
        """
        Return False if seat is occupied and has 5 or more occupied
        seats adjacent to it. Checks rule 2 for part 2.
        """
        row, col = location
        # TODO: fixes bug first version 1, test carefully
        if self.grid[row][col] != '#':
            return True
        neighbours = 0
        for move in self.moves:
            new_row = move[0] + row
            new_col = move[1] + col
            if (new_row, new_col) not in self.seats:
                continue
            val = self.visible_neighbours(location, move)
            if val == '#':
                neighbours += 1
                if neighbours > 4:
                    return False
        return True

    def locations_rule_one(self) -> List[Tuple]:
        """Return list with all locations that agree with rule one."""
        free_seats = []
        for loc in self.seats:
            if self.valid_empty_seat(loc):
                free_seats.append(loc)
        return free_seats

    def locations_rule_one_p2(self) -> List[Tuple]:
        """Return list with all locations that agree with rule one."""
        free_seats = []
        for loc in self.seats:
            if self.valid_empty_seat_two(loc):
                free_seats.append(loc)
        return free_seats

    def locations_rule_two(self) -> List[Tuple]:
        """Return list with all locations that agree with rule two."""
        busy_seats = []
        for loc in self.seats:
            if not self.too_many_neighbours(loc):
                busy_seats.append(loc)
        return busy_seats

    def locations_rule_two_p2(self) -> List[Tuple]:
        """Return list with all locations that agree with rule two."""
        busy_seats = []
        for loc in self.seats:
            if not self.too_many_neighbours_two(loc):
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
            # print("adjustments needed:", len(rule_one_locs), len(rule_two_locs))
            if len(rule_one_locs) + len(rule_two_locs) == 0:
                return self.occupied
            self.apply_changes(rule_one_locs, '#')
            self.apply_changes(rule_two_locs, 'L')
            # print("round", i, "occupied =", self.occupied)

    def modify_two(self, rounds: int) -> int:
        for i in range(rounds):
            rule_one_locs = self.locations_rule_one_p2()
            rule_two_locs = self.locations_rule_two_p2()
            print("adjustments needed:", len(rule_one_locs), len(rule_two_locs))
            if len(rule_one_locs) + len(rule_two_locs) == 0:
                return self.occupied
            self.apply_changes(rule_one_locs, '#')
            self.apply_changes(rule_two_locs, 'L')
            print("round", i, "occupied =", self.occupied)

    def __str__(self):
        floor_plan = ""
        for line in self.grid:
            floor_plan += f"{''.join(line)}\n"
        return floor_plan

    def __repr__(self):
        floor_plan = ""
        for line in self.grid:
            floor_plan += f"{line}\n"
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

t3_raw = """
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

t4_raw = """
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""

t0_list = [list(x.strip()) for x in t0_raw.strip().split()]
t1_list = [list(x.strip()) for x in t1_raw.strip().split()]
t2_list = [list(x.strip()) for x in t2_raw.strip().split()]
t3_list = [list(x.strip()) for x in t3_raw.strip().split()]
t4_list = [list(x.strip()) for x in t4_raw.strip().split()]
# print(t0_list)

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
# t0 = FloorPlan(t0_list)
# print(t0)
# t0.modify(2)
# t0.modify_two(2)
# print(t0)
# print(t0.occupied)
# print()

# t1 = FloorPlan(t1_list)
# print(t1)
# print(repr(t1))
# TODO: move to test file
# assert t1.visible_neighbours((4, 3), (1, 1)) == '#'
# assert t1.visible_neighbours((4, 3), (-1, 0)) == '#'
# assert t1.visible_neighbours((1, 1), (-1, 0)) == False
# assert t1.visible_neighbours((3, 3), (0, 1)) == False

# t3 = FloorPlan(t3_list)
# print(t3)
# print(sorted(t3.locations_rule_two_p2()))

t4 = FloorPlan(t4_list)
# print(t4)
# print(t4.valid_empty_seat((3, 8)))
# print(t4.valid_empty_seat_two((3, 8)))

if __name__ == '__main__':
    print()
    print('calculating...')
    day11_raw = file_reader('inputs/2020_11.txt', output='lines')
    day11_list = [list(x) for x in day11_raw]
    day11 = FloorPlan(day11_list)
    st = perf_counter()
    p1 = day11.modify(100)
    end = perf_counter()
    time1 = round(end - st, 1)
    print(f'solution part one: {p1} ({time1}ms)')
