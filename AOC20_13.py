from helpers import file_reader
from time import perf_counter
import heapq


def trips(time, limit):
    # TODO: helper can probably be removed
    all_times = []
    for t in range(0, limit, time):
        all_times.append(t)
    return all_times


def compute(etd, buses):
    next_bus_time = etd * 2
    next_bus = None
    for bus in buses:
        bus_trips = etd // bus
        next_departure = (bus_trips + 1) * bus
        if next_departure < next_bus_time:
            next_bus_time = next_departure
            next_bus = bus
    return (next_bus_time - etd) * next_bus


def calc_next_bus(timestamp, bus):
    trips_made = timestamp // bus
    return (trips_made + 1) * bus


def compute_two(data):
    """
    First part 2 solution. It works on test cases, but is way too slow
    for actual input.
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
        # print(current_time)
        # if current_time > 100000000:
        #     return "This is insane!"


def find_matches(first, other, index_other, limit):
    matches = []
    for x in range(0, 1000000, first):
        cur_sum = x + index_other
        if cur_sum % other == 0:
            matches.append(x)
        if len(matches) == limit:
            return matches
    return matches


def calc_step_size(first, big, big_index, mid, mid_index):
    matches = []
    for x in range(0, 1000000, first):
        cur_sum = x + big_index
        if cur_sum % big == 0:
            matches.append(x)
        if len(matches) == 2:
            break
    first_match = matches[0]
    step_size = matches[1] - matches[0]
    index_diff = mid_index - big_index
    # TODO: all below is new (original returned (first_match, step_size)
    stepper = (first_match + (step_size * i) for i in range(100000))
    next_match = 0
    for num in stepper:
        cur_sum = (num + mid_index) % mid == 0
        # cur_sum = (num - big_index) % first == 0
        if cur_sum:
            next_match = num
            break
    # print("start =", next_match)
    # print("step size =", first * big * mid)
    # return first_match, step_size
    return next_match, first * big * mid


def biggest_matches(first, first_index, other, index_other, limit):
    matches = []
    for x in range(0, 1000000, first):
        cur_sum = x + index_other
        if cur_sum % other == 0:
            matches.append(x)
        if len(matches) == limit:
            return matches
    return matches


# print(find_matches(7, 59, 4, 3))
# print(find_matches(19, 821, 19, 3))
# print(calc_step_size(7, 59, 4, 31, 6))
# print(calc_step_size(19, 821, 19, 463, 50))


def step_generator(start, step):
    """Generate steps from steps and step_size."""
    for i in range(84):
        yield start + (i * step)


# t66 = step_generator(350, 413)
# print(next(t66))
# print(next(t66))
# print(next(t66))
# for x in step_generator(6132, 12803):
#     print(x)


def compute_fast(data):
    buses = [int(a) for a in data if a != 'x']
    # times = [int(data[0]) + i for i, b in enumerate(data) if b != 'x']

    biggie, middie = heapq.nlargest(2, buses)
    # print(biggie, middie)

    offsets = {int(bus): i for i, bus in enumerate(data) if bus != 'x'}
    # print(buses)
    # print(offsets)
    # first_bus_time = current_time = buses[0]
    bus_count = len(buses)
    # biggie = max(buses)  # deactivated
    index_biggie = data.index(str(biggie))
    index_middie = data.index(str(middie))
    current_time, step = calc_step_size(buses[0], biggie, index_biggie, middie, index_middie)
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
        current_time += step
        # print(current_time)
        # if current_time > 100000000000:
        #     return "This is insane!"


"""
First idea to speed things up. Work with the largest bus in the list.
That way your steps are much bigger. ==> Rough calcs imply it will still take days.

Can we do something with the window? Size of the window is the number of buses ic

Produce a list with the values that need to be reached

"""

t0_time = 939
t0_buses = ['7', '13', 'x', 'x', '59', 'x', '31', '19']  # 1068781
t0_clean = [7, 13, 59, 31, 19]

t1 = ['17', 'x', '13', '19']  # 3417
t2 = ['67', '7', '59', '61']  # 754018
t3 = ['67', 'x', '7', '59', '61']  # 779210
t4 = ['67', '7', 'x', '59', '61']  # 1261476
t5 = ['1789', '37', '47', '1889']  # 1202161486
t6 = ['7', 'x', '3', 'x', 'x', '11', 'x', '5']


# assert compute_two(t0_buses) == 1068781
# assert compute_two(t1) == 3417
# assert compute_two(t2) == 754018
# assert compute_two(t3) == 779210
# assert compute_two(t4) == 1261476
# assert compute_two(t5) == 1202161486

# print(compute_two(t0_buses))
# print(compute_two(t1))
# print(compute_two(t2))
# print(compute_two(t6))


# print(t0_buses)
# print(compute_two(t0_buses))
#
# print(compute_fast(t0_buses))
# print(compute_fast(t1))
# print(compute_fast(t2))
# print(compute_fast(t3))
# print(compute_fast(t4))


# print(calc_next_bus(17, 13))

day13_raw = file_reader('inputs/2020_13.txt', output='lines')
day13_time = int(day13_raw[0])
day13_buses = [bus for bus in day13_raw[1].split(',')]
# day13_clean = [int(bus) for bus in day13_raw[1].split(',') if bus != 'x']
# day13_tups = [(int(bus), i) for i, bus in enumerate(day13_buses) if bus != 'x']
# assert compute(t0_time, t0_clean) == 295
# print("part 1 answer:", compute(day13_time, day13_clean))
# print("To get solution for part 2 un-comment lines 206-211")
# print("WARNING: it will take 3+ minutes!!")

# start = perf_counter()
# TODO: run the below line to get the answer for part 2 (WARNING: will take 3+ minutes!!)
# TODO: only later realized only prime number seem to be used. Impact?
# p2 = compute_fast(day13_buses)
# end = perf_counter()
# print(p2)
# print(end - start)


def first_match(other, index_other, base, base_index=0, max_size=1000000):
    """
    Find first match of . Always return the value based
    """
    # step = max(other, base)
    step = other
    index_diff = index_other - base_index
    for value in range(step, max_size, step):
        base_value = value - index_diff
        if base_value % base == 0:
            return value - index_diff


def bus_match(data):
    first_bus = int(data[0])
    later_buses = [(int(bus), i) for i, bus in enumerate(data[1:], start=1) if bus != 'x']
    bus_order = sorted(later_buses, key=lambda x: x[0], reverse=True)
    biggest = bus_order[0]
    time = first_match(biggest[0], biggest[1], first_bus)
    step_size = first_bus * biggest[0]
    for bus in bus_order[1:]:
        while True:
            bus_time = time + bus[1]
            if bus_time % bus[0] == 0:
                time = bus_time - bus[1]
                step_size = step_size * bus[0]
                # print(bus, time, step_size)
                break
            time += step_size
    return time


assert first_match(13, 1, 7) == 77
assert first_match(59, 4, 7) == 350
assert first_match(31, 6, 7) == 56
assert first_match(19, 7, 7) == 126

print(bus_match(t0_buses))
print(bus_match(t1))
print(bus_match(t2))
print(bus_match(t3))
print(bus_match(t4))
print(bus_match(t6))

print(bus_match(day13_buses))
