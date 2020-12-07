import time
from collections import deque
from helpers import file_reader
from typing import Tuple, Dict, List, Deque


def get_bag_info(description: str) -> Tuple:
    """Return tuple with bag name and list of it's children"""
    description = description.replace("contain", ",")
    for word in ("bags", "bag", "."):
        description = description.replace(word, "")
    clean_bag_data = [x.strip() for x in description.split(",")]
    parent, *children = clean_bag_data
    if children[0] == "no other":
        return parent, None
    col_list = []
    for bag in children:
        number, *rest = bag.split(" ")
        color = " ".join(rest)
        col_list.append((color, int(number)))
    return parent, col_list


def build_graph(all_bag_descriptions: List) -> Dict:
    """Return graph with all child bags that each parent bag can contain."""
    bags_graph = {}
    for description in all_bag_descriptions:
        parent, children = get_bag_info(description)
        bags_graph[parent] = children
    return bags_graph


def compute_one(graph: Dict, target: str) -> int:
    """
    Return number of bags that contain target, using Breadth First Search.
    """
    # exclude target from search space, otherwise counted twice
    all_parents = [x for x in graph.keys() if x != target]
    bag_count = 0
    for parent in all_parents:
        frontier: Deque[str] = deque()
        frontier.append(parent)
        seen = {parent}
        while frontier:
            bag = frontier.popleft()
            if bag == target:
                bag_count += 1
                break
            if graph[bag]:
                for child in graph[bag]:
                    if child[0] not in seen:
                        frontier.append(child[0])
                        seen.add(child[0])
    return bag_count


def compute_two(graph: Dict, source: str) -> int:
    """
    Return number of bags held within target bag, using a modified
    Breadth First Search approach.
    """
    bag_count = 0
    frontier: Deque[Tuple] = deque()
    for kid in graph[source]:
        name, num = kid
        node = (source, name, num)
        frontier.append(node)
    while frontier:
        parent, name, value = frontier.popleft()
        bag_count += value
        if graph[name]:
            for child in graph[name]:
                child_name, child_value = child
                node = (name, child_name, value * child_value)
                frontier.append(node)
    return bag_count


if __name__ == "__main__":
    t0 = [
        "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags.",
    ]

    t1 = [
        "shiny gold bags contain 2 dark red bags.",
        "dark red bags contain 2 dark orange bags.",
        "dark orange bags contain 2 dark yellow bags.",
        "dark yellow bags contain 2 dark green bags.",
        "dark green bags contain 2 dark blue bags.",
        "dark blue bags contain 2 dark violet bags.",
        "dark violet bags contain no other bags.",
    ]

    t0_graph = build_graph(t0)
    t1_graph = build_graph(t1)
    assert compute_one(t0_graph, "shiny gold") == 4
    assert compute_two(t0_graph, "shiny gold") == 32
    assert compute_two(t1_graph, "shiny gold") == 126

    start = time.perf_counter()
    day7 = file_reader("inputs/2020_7.txt", output="lines")
    # TODO: Time p1 and p2 separately
    day7_graph = build_graph(day7)
    p1 = compute_one(day7_graph, "shiny gold")
    p2 = compute_two(day7_graph, "shiny gold")
    end = time.perf_counter()
    run_time = round((end - start) * 1000, 1)
    print("solution part 1:", p1)
    print("solution part 2:", p2)
    print(f"runtime: {run_time}ms")
