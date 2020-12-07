from collections import deque
from helpers import file_reader
from pprint import pprint


def bag_mapper(data):
    c1 = data.replace('contain', ',')
    c1 = c1.replace('bags.', '')
    c1 = c1.replace('bags', '')
    c1 = c1.replace('bag.', '')
    c1 = c1.replace('bag', '')
    c1_list = [x.strip() for x in c1.split(',')]
    key_bag, *other = c1_list
    if other[0] == 'no other':
        return key_bag, None
    col_list = []
    for bag in other:
        number, *rest = bag.split(' ')
        color = " ".join(rest)
        # col_dict[color] = int(number)
        col_list.append((color, int(number)))
    return key_bag, col_list


def full_bag_data(data):
    bags_dict = {}
    for line in data:
        bag, colors = bag_mapper(line)
        bags_dict[bag] = colors
    return bags_dict


def find_all_paths(bags_dict, path, all_paths=[]):
    """recursive algorithm that finds all possible paths in graph"""
    # TODO: remove
    cur_bag = path[-1]
    color, count = cur_bag
    if bags_dict[color]:
        for bag in bags_dict[color]:
            new_path = path + [bag]
            find_all_paths(bags_dict, new_path, all_paths)
    else:
        all_paths += [path]
    return all_paths


def compute(data, target):
    color_map = full_bag_data(data)
    bag_count = 0
    for color in color_map.keys():
        frontier = deque()
        if color_map[color]:
            for c in color_map[color]:
                frontier.append(c)
            # print(frontier)
            while frontier:
                cur_bag = frontier.popleft()
                cur_col, num = cur_bag
                if cur_col == target and num > 0:
                    bag_count += 1
                    break
                else:
                    children = color_map[cur_col]
                    if children:
                        for child in children:
                            frontier.append(child)
    return bag_count


def compute_two(data, source):
    bag_dict = full_bag_data(data)
    bag_count = 0
    frontier = deque()
    seen = set()
    for kid in bag_dict[source]:
        name, num = kid
        node = (source, name, num)
        frontier.append(node)
        seen.add(node)
    while frontier:
        parent, name, value = frontier.popleft()
        bag_count += value
        if bag_dict[name]:
            for child in bag_dict[name]:
                child_name, child_value = child
                node = (name, child_name, value * child_value)
                frontier.append(node)
                seen.add(node)
    return bag_count


t0_raw = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

t0 = [x for x in t0_raw.strip().split('\n')]

# t0_bags_dict = full_bag_data(t0)
# pprint(find_all_paths(t0_bags_dict, [('shiny gold', 1)]))

assert compute(t0, 'shiny gold') == 4
assert compute_two(t0, 'shiny gold') == 32

day7 = file_reader('inputs/2020_7.txt', output='lines')
print(compute(day7, 'shiny gold'))
print(compute_two(day7, 'shiny gold'))
