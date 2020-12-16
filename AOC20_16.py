from helpers import file_reader
from typing import List
from pprint import pprint


def field_ranges(data: List[str]):
    field_data = {}
    for line in data:
        description, values = line.split(': ')
        range_strings = values.split(' or ')
        ranges = []
        for r in range_strings:
            low, high = r.split('-')
            ranges.append((int(low), int(high)))
        field_data[description] = ranges
    return field_data


def compute(field_data, nearby, error_rate=True):
    """Return error rate. Solution part 1."""
    field_values = field_ranges(field_data).values()
    ranges = []
    for field in field_values:
        for r in field:
            ranges.append(r)
    invalid = []
    for ticket in nearby:
        valid = False
        for ran in ranges:
            low, high = ran
            if low <= ticket <= high:
                valid = True
                break
        if not valid:
            invalid.append(ticket)
    # print(invalid)
    # return sum(invalid)
    return sum(invalid) if error_rate else invalid


def compute_two(data):
    pass


"""
NOTES:

There are almost no test cases. I will need to be very careful not to make
any mistakes. Perhaps build own tests.

* Each line in other tickets represents a ticket with 20 fields (CHECK!)
* In part one you found the values that are not contained in any range.
  All tickets (lines) that contain one of these values should be discarded.
* Build a 2d list with all the valid tickets (lines).
* We will compare the fields of the tickets, ie position 0 for every ticket,
  position 1 for every ticket etc. To make this easier the 2d list of tickets
  should be transposed. That way every line becomes a potential field.
  Therefore this 2d list should have 20 rows.
* 

"""

t0_raw = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

t0_parts = [part.strip() for part in t0_raw.strip().split('\n\n')]
t0_others_raw = t0_parts[2].split(':\n')
t0_other_ticket_strings = t0_others_raw[1].replace('\n', ',')
t0_fields = [field.strip() for field in t0_parts[0].strip().split('\n')]
t0_other = [int(ticket) for ticket in t0_other_ticket_strings.split(',')]


day16_raw = file_reader('inputs/2020_16.txt')
day16_parts = [part.strip() for part in day16_raw.strip().split(('\n\n'))]
# print(day16_parts[0])
day16_others_raw = day16_parts[2].split(':\n')
# print(day16_others_raw)
day16_other_ticket_strings = day16_others_raw[1].replace('\n', ',')
# print(day16_other_ticket_strings)

day16_fields = [field.strip() for field in day16_parts[0].strip().split('\n')]
# print(day16_fields)
day16_other = [int(ticket) for ticket in day16_other_ticket_strings.split(',')]
# print(day16_other)

# PART 1
assert compute(t0_fields, t0_other) == 71
print(compute(day16_fields, day16_other))
print(compute(day16_fields, day16_other, error_rate=False))
