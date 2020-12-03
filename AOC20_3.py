from helpers import file_reader
from math import prod


def compute(data):
    height = len(data)
    width = len(data[0])
    row = col = 0
    trees = 0
    while row < height:
        if data[row][col] == '#':
            trees += 1
        row += 1
        col = (col + 3) % width
    return trees


def compute_two(data):
    height = len(data)
    width = len(data[0])
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    row = col = 0
    maps = []
    for slope in slopes:
        trees = 0
        row = col = 0
        while row < height:
            if data[row][col] == '#':
                trees += 1
            row_delta, col_delta = slope
            row += row_delta
            col = (col + col_delta) % width
        maps.append(trees)
    # print(maps)
    return prod(maps)


if __name__ == '__main__':
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
    t0 = t0_raw.strip().split('\n')
    # print(t0)

    # assert compute(t0) == 7
    # print(compute(t0))
    # assert compute_two(t0) == 336
    #
    day3 = file_reader('inputs/2020_3.txt', output='lines')
    print(compute(day3))
    print(compute_two(day3))
