from helpers import file_reader
from collections import Counter


def compute(data):
    count = []
    for group in data:
        person_count = set()
        for person in group:
            for letter in person:
                person_count.add(letter)
        count.append((len(person_count)))
    return sum(count)


def compute_two(data):
    count = []
    for group in data:
        size_group = len(group)
        # print('size_group =', size_group)
        q_count = Counter()
        for person in group:
            for letter in person:
                q_count[letter] += 1
        group_count = 0
        for lc in q_count.values():
            if lc == size_group:
                group_count += 1
        count.append(group_count)
    return sum(count)


t0_raw = """abc

a
b
c

ab
ac

a
a
a
a

b
"""

if __name__ == '__main__':
    t0_groups = [x.strip() for x in t0_raw.split('\n\n')]
    t0 = [x.split('\n') for x in t0_groups]
    assert compute(t0) == 11
    assert compute_two(t0) == 6

    day6_raw = file_reader('inputs/2020_6.txt')
    day6_groups = [x.strip() for x in day6_raw.split('\n\n')]
    day6 = [x.split('\n') for x in day6_groups]
    print((compute(day6)))
    print(compute_two(day6))
