import pytest
from AOC20_11 import FloorPlan

test0_raw = """
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

test1_raw = """
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

test2_raw = """
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
"""

test3_raw = """
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

test4_raw = """
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

test5_raw = """
L.L...
.L..#.
..L...
#.#.#L
...LLL
#..L..
"""

test0_list = [list(x.strip()) for x in test0_raw.strip().split()]
test1_list = [list(x.strip()) for x in test1_raw.strip().split()]
test2_list = [list(x.strip()) for x in test2_raw.strip().split()]
test3_list = [list(x.strip()) for x in test3_raw.strip().split()]
test4_list = [list(x.strip()) for x in test4_raw.strip().split()]
test5_list = [list(x.strip()) for x in test5_raw.strip().split()]

fp0 = FloorPlan(test0_list)
fp1 = FloorPlan(test1_list)
fp2 = FloorPlan(test2_list)
fp3 = FloorPlan(test3_list)
fp4 = FloorPlan(test4_list)
fp5 = FloorPlan(test5_list)


# print(fp5)
# print(fp5.valid_empty_seat((0, 0)))
# print(fp5.valid_empty_seat((3, 8)))
# print(fp5.valid_empty_seat((7, 8)))

def test_fp0_height():
    assert fp0.height == 10


def test_fp0_occupied():
    assert fp0.occupied == 0


def test_fp1_occupied():
    assert fp1.occupied == 8


def test_fp4_occupied():
    assert fp4.occupied == 31


@pytest.mark.parametrize('loc, move, expected', (
        pytest.param((0, 0), (-1, 0), False),
        pytest.param((3, 3), (0, -1), False),
        pytest.param((4, 5), (0, -1), "L"),
        pytest.param((4, 5), (0, 1), "#"),
        pytest.param((4, 5), (-1, 0), False),
        pytest.param((4, 5), (1, 0), False),
        pytest.param((4, 5), (1, -1), "#"),
        pytest.param((4, 0), (-1, 1), "#"),
))
def test_fp1_visible_neighbours(loc, move, expected):
    """
    Return the first seat you see from location in direction of move.
    Should return:
        'L' if empty
        '#' if occupied
        False if none found
    """
    assert fp1.visible_neighbours(loc, move) == expected


@pytest.mark.parametrize('loc, move, expected', (
        pytest.param((3, 8), (-1, -1), "#"),
        pytest.param((3, 8), (0, 1), "#"),
        pytest.param((3, 8), (1, 1), "#"),
        pytest.param((3, 8), (1, 0), "L")
))
def test_fp4_visible_neighbours(loc, move, expected):
    """
    Return the first seat you see from location in direction of move.
    Should return:
        'L' if empty
        '#' if occupied
        False if none found
    """
    assert fp4.visible_neighbours(loc, move) == expected


@pytest.mark.parametrize('test_input, expected', (
        pytest.param((0, 0), False),
        pytest.param((3, 8), False),
        pytest.param((7, 8), False),
        pytest.param((0, 5), False),
        pytest.param((2, 2), False)
))
def test_fp4_valid_empty_seat_p2(test_input, expected):
    assert fp4.valid_empty_seat_two(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        pytest.param((0, 0), True),
        pytest.param((0, 3), True),
        pytest.param((4, 5), True),
        pytest.param((5, 5), True),
        pytest.param((2, 2), True)
))
def test_fp4_too_many_neighbours_p2(test_input, expected):
    assert fp4.too_many_neighbours_two(test_input) == expected


@pytest.mark.parametrize('test_input, expected', (
        pytest.param((0, 0), True),
        pytest.param((3, 0), False),
        pytest.param((3, 5), False),
        pytest.param((0, 1), False),
        pytest.param((5, 3), True)
))
def test_fp5_valid_empty_seat(test_input, expected):
    assert fp5.valid_empty_seat(test_input) == expected


@pytest.mark.parametrize('location, expected', (
        pytest.param((0, 0), False),
        pytest.param((1, 1), True),
        pytest.param((3, 0), False),
        pytest.param((3, 5), False),
        pytest.param((0, 1), False),
        pytest.param((5, 3), False)
))
def test_fp5_valid_empty_seat_p2(location, expected):
    assert fp5.valid_empty_seat_two(location) == expected
