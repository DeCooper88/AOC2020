from helpers import file_reader
from typing import List
from time import perf_counter


def compute(departure: int, all_buses: List[str]) -> int:
    """
    Return ID of the earliest bus you can take to the airport multiplied
    by the number of minutes you'll need to wait for that bus.
    Solution part 1.
    """
    buses = [int(bus) for bus in all_buses if bus != 'x']
    next_bus_time = departure * 2
    next_bus = int
    for bus in buses:
        bus_trips = departure // bus
        next_departure = (bus_trips + 1) * bus
        if next_departure < next_bus_time:
            next_bus_time = next_departure
            next_bus = bus
    return (next_bus_time - departure) * next_bus


def compute_slow(data: List[str]) -> int:
    """
    First solution for part 2. It works on all test cases, but is way too
    slow for actual input. (Calculation would take days!!)
    """
    buses = [int(a) for a in data if a != 'x']
    first_bus_time = current_time = buses[0]
    bus_count = len(buses)
    offsets = {int(bus): time for time, bus in enumerate(data) if bus != 'x'}
    while True:
        count = 0
        for bus in buses[1:]:
            correct_time = current_time + offsets[bus]
            if correct_time % bus == 0:
                count += 1
            else:
                break
            if count == bus_count - 1:
                return current_time
        current_time += first_bus_time


def first_match(other: int, index_other: int, base: int, base_index=0, max_size=1000000) -> int:
    """
    Find first time on which the first bus and the largest bus match. Return time
    of the first bus.
    """
    step = other
    index_diff = index_other - base_index
    for value in range(step, max_size, step):
        base_value = value - index_diff
        if base_value % base == 0:
            return value - index_diff
    raise AssertionError("No match is possible")


def compute_two(data: List[str]):
    """
    Return earliest timestamp such that all of the listed bus IDs depart
    at offsets matching their positions in the list.
    This is a fast solution for part 2. The algorithm works as follows:
        1) find the earliest time at which the first bus in the list
           matches the time of the largest bus (max bus ID) in the
           list;
        2) make step_size the product of these bus IDs, ie if the buses
           were 7 and 59, the step_size becomes 413;
        3) from the first match time, iterate with steps of step_size
           until you match the bus with the next largest ID;
        4) modify time;
        5) multiply step_size by ID current bus;
        5) keep repeating this until you reach the smallest bus.
    """
    first_bus = int(data[0])
    later_buses = [(int(bus), i) for i, bus in enumerate(data[1:], start=1) if bus != 'x']
    bus_order = sorted(later_buses, key=lambda x: x[0], reverse=True)
    biggest_bus, biggest_bus_index = bus_order[0]
    time = first_match(biggest_bus, biggest_bus_index, first_bus)
    step_size = first_bus * biggest_bus
    for bus in bus_order[1:]:
        while True:
            bus_id, offset = bus
            bus_time = time + offset
            if bus_time % bus_id == 0:
                time = bus_time - offset
                step_size = step_size * bus_id
                break
            time += step_size
    return time


assert first_match(13, 1, 7) == 77
assert first_match(59, 4, 7) == 350
assert first_match(31, 6, 7) == 56
assert first_match(19, 7, 7) == 126

t0 = ['7', '13', 'x', 'x', '59', 'x', '31', '19']  # 1068781
t1 = ['17', 'x', '13', '19']  # 3417
t2 = ['67', '7', '59', '61']  # 754018
t3 = ['67', 'x', '7', '59', '61']  # 779210
t4 = ['67', '7', 'x', '59', '61']  # 1261476
t5 = ['7', 'x', '3', 'x', 'x', '11', 'x', '5']  # 28


if __name__ == '__main__':
    assert compute(939, t0) == 295

    assert compute_slow(t0) == 1068781
    assert compute_slow(t1) == 3417
    assert compute_slow(t2) == 754018
    assert compute_slow(t3) == 779210
    assert compute_slow(t4) == 1261476
    assert compute_slow(t5) == 28

    assert compute_two(t0) == 1068781
    assert compute_two(t1) == 3417
    assert compute_two(t2) == 754018
    assert compute_two(t3) == 779210
    assert compute_two(t4) == 1261476
    assert compute_two(t5) == 28

    day13_raw = file_reader('inputs/2020_13.txt', output='lines')
    day13 = [bus for bus in day13_raw[1].strip().split(',')]

    st = perf_counter()
    print("part 1 answer:", compute(1001612, day13))
    print("part 2 answer:", compute_two(day13))
    end = perf_counter()
    print(f"runtime is {round((end - st) * 1000, 1)}ms")
