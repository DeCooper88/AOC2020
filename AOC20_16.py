from helpers import file_reader
from typing import Dict, List, Set
from pprint import pprint
from math import prod


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
    return sum(invalid) if error_rate else set(invalid)


def get_other_tickets(data: str) -> List[List[int]]:
    """
    Return 2D list with other tickets data. Helper function part 2.
    """
    all = data.strip().split('\n\n')
    _, other = all[2].split(':\n')
    ticket_strings = [t.strip() for t in other.split('\n')]
    ticket_list = []
    for ts in ticket_strings:
        ticket = [int(t) for t in ts.split(',')]
        ticket_list.append(ticket)
    return ticket_list


def filter_invalid_tickets(tickets: List, errors: Set) -> List:
    """Return list of tickets without errors."""
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for field in ticket:
            if field in errors:
                valid = False
                # print("wrong ticket:", ticket)
                break
        if valid:
            valid_tickets.append(ticket)
    return valid_tickets


def list_by_fields(tickets):
    """return transposed list of tickets"""
    return [list(i) for i in zip(*tickets)]


def possible_fields_for_row(row: List, fields: Dict):
    """Return list of data_fields that row is valid for."""
    valid_fields = []
    for field, ranges in fields.items():
        all_valid = True
        for num in row:
            found = 0
            for ran in ranges:
                low, high = ran
                if low <= num <= high:
                    found += 1
            if found == 0:
                all_valid = False
                break
        if all_valid:
            valid_fields.append(field)
    return valid_fields


t2_fields = {'class': [(0, 1), (4, 19)], 'row': [(0, 5), (8, 19)], 'seat': [(0, 13), (16, 19)]}
t2_transposed_list = [[3, 15, 5], [9, 1, 14], [18, 5, 9]]

assert possible_fields_for_row(t2_transposed_list[0], t2_fields) == ['row']
assert possible_fields_for_row(t2_transposed_list[1], t2_fields) == ['class', 'row']
assert possible_fields_for_row(t2_transposed_list[2], t2_fields) == ['class', 'row', 'seat']


def map_fields(field_strings: List[str], valid_tickets: List):
    data_fields = field_ranges(field_strings)
    field_rows = list_by_fields(valid_tickets)
    mapper = {}  # field_row: [possible data_fields]
    for i, row in enumerate(field_rows):
        options = possible_fields_for_row(row, data_fields)
        mapper[i] = options
    return mapper


def find_indices(table: Dict):
    seen = set()
    mapper = {}
    while len(seen) < 20:
        for loc, fields in table.items():
            if loc in mapper:
                continue
            current = set(fields)
            set_diff = current - seen
            if len(set_diff) == 1:
                f = set_diff.pop()
                mapper[loc] = f
                seen.add(f)
    return mapper


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

t1_raw = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

t0_parts = [part.strip() for part in t0_raw.strip().split('\n\n')]
t0_others_raw = t0_parts[2].split(':\n')
t0_other_ticket_strings = t0_others_raw[1].replace('\n', ',')
t0_fields = [field.strip() for field in t0_parts[0].strip().split('\n')]
t0_other = [int(ticket) for ticket in t0_other_ticket_strings.split(',')]

day16_raw = file_reader('inputs/2020_16.txt')
# print(type(day16_raw))
day16_parts = [part.strip() for part in day16_raw.strip().split(('\n\n'))]
# print(day16_parts[0])
day16_others_raw = day16_parts[2].split(':\n')
# print(day16_others_raw)
day16_other_ticket_strings = day16_others_raw[1].replace('\n', ',')
# print(day16_other_ticket_strings)
day16_fields = [field.strip() for field in day16_parts[0].strip().split('\n')]
# print(day16_fields)
day_16_all_other_fieldnums = [int(ticket) for ticket in day16_other_ticket_strings.split(',')]

day16_all_other_tickets = get_other_tickets(day16_raw)
day16_wrong_numbers = compute(day16_fields, day_16_all_other_fieldnums, error_rate=False)
day16_valid_tickets = filter_invalid_tickets(day16_all_other_tickets, day16_wrong_numbers)
day16_valids_by_field = list_by_fields(day16_valid_tickets)
day16_table = map_fields(day16_fields, day16_valid_tickets)
day16_mapped = find_indices(day16_table)


def compute_two(data):
    pass


# PART 1
assert compute(t0_fields, t0_other) == 71
p1 = compute(day16_fields, day_16_all_other_fieldnums)
print("solution part 1:", p1)
# print(compute(day16_fields, day_16_all_other_fieldnums, error_rate=False))


# print(day16_mapped)
deps = [i for i, f in day16_mapped.items() if f.startswith('departure')]
# print(sorted(deps))
my_ticket = [163, 73, 67, 113, 79, 101, 109, 149, 53, 61, 97, 89, 103, 59, 71, 83, 151, 127, 157, 107]

ajax = []
for i in deps:
    ajax.append(my_ticket[i])

# print(ajax)
p2 = prod(ajax)
print("solution part 2:", p2)

t1_parts = [part.strip() for part in t1_raw.strip().split('\n\n')]
t1_fields = [field.strip() for field in t1_parts[0].strip().split('\n')]
t1_all_other = get_other_tickets(t1_raw)
# print(t1_fields)
# print(t1_all_other)


# print(map_fields(t1_fields, t1_all_other))

# pprint(map_fields(day16_fields, day16_valids_by_field))

# print(t1_all_other)
# print(list_by_fields(t1_all_other))


# print(day16_all_other_tickets)
# print(len(day16_all_other_tickets))
# print(day16_wrong_numbers)
# print()
# print(len(day16_valid_tickets))
# print(len(day16_valids_by_field))


# print(sorted(day16_valids_by_field[0]))
# pprint(field_ranges(day16_fields))
# for x in day16_valids_by_field:
#     # print(len(x))
#     print(min(x))
#     print(max(x))
#     print(sorted(x[:10]))


# for i, line in day16_table.items():
#     print(i, len(line))
#     print(line)
#     print()
