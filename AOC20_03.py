from typing import List, Tuple
import numpy as np
from time import perf_counter


def get_input(data_file: str) -> List[str]:
    """Return content data_file as list of strings."""
    with open(data_file) as f:
        return [x.strip() for x in f.readlines()]


def trees_seen(grid: List[str], slopes: List[Tuple[int, int]]):
    """
    Find number of trees encountered on grid whilst traversing it by
    certain slopes. Return the product of the trees encounter per slope.
    """
    height, width = len(grid), len(grid[0])
    trees_per_slope = []
    for slope in slopes:
        trees = row = col = 0
        row_delta, col_delta = slope
        while row < height:
            if grid[row][col] == "#":
                trees += 1
            row += row_delta
            col = (col + col_delta) % width
        trees_per_slope.append(trees)
    return np.prod(trees_per_slope)


if __name__ == "__main__":
    t0_raw = """
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
    """
    t0 = [x.strip() for x in t0_raw.strip().split("\n")]
    # tests:
    assert trees_seen(t0, [(1, 3)]) == 7
    assert trees_seen(t0, [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]) == 336

    start = perf_counter()
    day3 = get_input("inputs/2020_3.txt")
    sp1 = perf_counter()
    p1 = trees_seen(day3, [(1, 3)])
    sp2 = perf_counter()
    p2 = trees_seen(day3, [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)])
    end = perf_counter()

    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms")
