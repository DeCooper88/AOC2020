from helpers import file_reader


def calc_id(data):
    rows = data[:7]
    # print(rows)
    seats = data[7:]
    low, high = 0, 127
    for step in rows:
        if step == 'F':  # lower half
            high = (high + low) // 2
        elif step == 'B':  # upper half
            low = ((high + low) // 2) + 1
        # print(low, high)
    assert low == high
    left, right = 0, 7
    for seat in seats:
        if seat == 'L':  # lower half
            right = (left + right) // 2
        elif seat == 'R':  # upper half
            left = ((left + right) // 2) + 1
        # print(left, right)
    assert left == right
    return (low * 8) + left


def compute(data):
    highest_id = 0
    for bp in data:
        bp_id = calc_id(bp)
        highest_id = max(bp_id, highest_id)
    return highest_id


def compute_two(data):
    seen = set()
    all_seats = set(range(1024))
    for bp in data:
        bp_id = calc_id(bp)
        seen.add(bp_id)
    not_seen = all_seats - seen
    too_low = 128
    too_high = (8 * 128) - 128
    potentials = []
    for seat_id in not_seen:
        if too_low < seat_id < too_high:
            potentials.append(seat_id)
    assert len(potentials) == 1
    return potentials[0]


if __name__ == '__main__':
    t0 = 'FBFBBFFRLR'
    t1 = 'BFFFBBFRRR'
    t2 = 'FFFBBBFRRR'
    t3 = 'BBFFBBFRLL'
    all_tests = [t0, t1, t2, t3]

    assert calc_id(t0) == 357
    assert calc_id(t1) == 567
    assert calc_id(t2) == 119
    assert calc_id(t3) == 820

    assert compute(all_tests) == 820

    day5 = file_reader('inputs/2020_5.txt', output='lines')
    print(compute(day5))
    print(compute_two(day5))
