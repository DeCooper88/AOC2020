from helpers import file_reader
import math
import time


def trees_seen(grid, slopes):
    """
    Return number of trees encountered on grid whilst traversing it by
    certain slopes. If len(slopes) == 1 return the number of trees
    encountered, else return the product of the trees encounter per slope.
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
    return math.prod(trees_per_slope)


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
    assert trees_seen(t0, ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))) == 336

    day3 = file_reader("inputs/2020_3.txt", output="lines")

    start = time.perf_counter()
    p1 = trees_seen(day3, [(1, 3)])
    middle = time.perf_counter()
    p2 = trees_seen(day3, [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)])
    end = time.perf_counter()

    t1 = int((middle - start) * 1000)
    t2 = int((end - middle) * 1000)
    print(f"solution part 1: {p1} ({t1}ms)")
    print(f"solution part 2: {p2} ({t2}ms)")
