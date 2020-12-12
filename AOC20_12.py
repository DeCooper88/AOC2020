from helpers import file_reader
from typing import List, NamedTuple, Tuple
from time import perf_counter


class Move(NamedTuple):
    direction: str
    size: int


def get_info(data: List[str]) -> List[Move]:
    """Convert list of strings to list of Move(s) (=NamedTuple)"""
    all_instructions = []
    for x in data:
        instruction = x[0]
        amount = x[1:]
        move = Move(instruction, int(amount))
        all_instructions.append(move)
    return all_instructions


def direction_change(turn: str, direction: str, degrees: int) -> str:
    """
    Return new direction. Helper function part 1.
    """
    if turn == 'L':
        degrees = 360 - degrees
    directions = ['N', 'E', 'S', 'W', 'N', 'E', 'S', 'W']
    cur_idx = directions.index(direction)
    steps = int(degrees / 90)
    return directions[cur_idx + steps]


def calc_waypoint(way_point: List[int], turn: str, degrees: int) -> List[int]:
    """Return new way point. Helper function part 2."""
    # TODO: can probably improve this function with boolean logic
    if turn == 'L':
        degrees = 360 - degrees
    steps = int(degrees / 90)
    old_x, old_y = way_point
    if old_x > 0:
        a = 1
    elif old_x < 0:
        a = -1
    else:
        a = 0
    if old_y > 0:
        b = 1
    elif old_y < 0:
        b = -1
    else:
        b = 0
    quadrant = (a, b)
    # North, East, South, West, North etc..
    regulars = ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 1), (1, 0), (0, -1), (-1, 0))
    # NE, SE, SW, NW, NE etc...
    offsets = ((1, 1), (1, -1), (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1), (-1, 1))
    new_quadrant = Tuple
    if quadrant in offsets:
        location = offsets.index(quadrant)
        new_quadrant = offsets[location + steps]
    elif quadrant in regulars:
        location = regulars.index(quadrant)
        new_quadrant = offsets[location + steps]
    x, y = new_quadrant
    if steps == 2:
        return [abs(old_x) * x, abs(old_y) * y]
    return [abs(old_y) * x, abs(old_x) * y]


def compute(data: List[str]) -> int:
    """Day 12 part 1"""
    # TODO: refactor away all these if statements
    instructions = get_info(data)
    ship_faces = 'E'
    position = [0, 0]
    for move in instructions:
        if move.direction == 'L' or move.direction == 'R':
            ship_faces = direction_change(move.direction, ship_faces, move.size)
        elif move.direction == 'N':
            position[0] += move.size
        elif move.direction == 'S':
            position[0] -= move.size
        elif move.direction == 'E':
            position[1] += move.size
        elif move.direction == 'W':
            position[1] -= move.size
        elif move.direction == 'F':
            if ship_faces == 'N':
                position[0] += move.size
            elif ship_faces == 'S':
                position[0] -= move.size
            elif ship_faces == 'E':
                position[1] += move.size
            elif ship_faces == 'W':
                position[1] -= move.size
    return abs(position[0]) + abs(position[1])


def compute_two(data: List[str]) -> int:
    """Day 12 part 2"""
    # TODO: refactor away all these if statements
    instructions = get_info(data)
    way_point = [10, 1]
    position = [0, 0]
    for move in instructions:
        if move.direction == 'L' or move.direction == 'R':
            way_point = calc_waypoint(way_point, move.direction, move.size)
        elif move.direction == 'N':
            way_point[1] += move.size
        elif move.direction == 'S':
            way_point[1] -= move.size
        elif move.direction == 'E':
            way_point[0] += move.size
        elif move.direction == 'W':
            way_point[0] -= move.size
        elif move.direction == 'F':
            x = way_point[0] * move.size
            y = way_point[1] * move.size
            position[0] += x
            position[1] += y
    return abs(position[0]) + abs(position[1])


if __name__ == '__main__':
    assert calc_waypoint([3, 2], 'R', 90) == [2, -3]
    assert calc_waypoint([3, 2], 'L', 270) == [2, -3]
    assert calc_waypoint([3, 2], 'R', 180) == [-3, -2]
    assert calc_waypoint([3, 2], 'L', 90) == [-2, 3]
    assert calc_waypoint([10, 4], 'R', 90) == [4, -10]
    assert calc_waypoint([10, 4], 'L', 270) == [4, -10]
    assert calc_waypoint([10, 4], 'L', 180) == [-10, -4]
    assert calc_waypoint([10, -2], 'R', 90) == [-2, -10]
    assert calc_waypoint([10, -2], 'R', 180) == [-10, 2]
    assert calc_waypoint([3, 0], 'R', 90) == [0, -3]
    assert calc_waypoint([3, 0], 'L', 270) == [0, -3]

    assert direction_change('R', 'N', 90) == 'E'
    assert direction_change('L', 'N', 90) == 'W'
    assert direction_change('R', 'E', 180) == 'W'
    assert direction_change('L', 'E', 180) == 'W'
    assert direction_change('R', 'S', 270) == 'E'
    assert direction_change('L', 'S', 270) == 'W'

    t0 = ['F10', 'N3', 'F7', 'R90', 'F11']
    t1 = ['F10', 'N3', 'F7', 'L90', 'F11']
    t2 = ['F10', 'S3', 'F7', 'L90', 'F11']

    assert compute(t0) == 25
    assert compute_two(t0) == 286
    assert compute_two(t1) == 274

    start = perf_counter()
    day12_raw = file_reader('inputs/2020_12.txt', output='lines')
    p1 = compute(day12_raw)
    p2 = compute_two(day12_raw)
    end = perf_counter()
    runtime = round((end - start) * 1000, 1)
    print(f"solution part 1: {p1}")
    print(f"solution part 2: {p2}")
    print(f"runtime: {runtime}ms")
