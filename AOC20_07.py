from collections import deque
from typing import Deque, Dict, Iterable, Tuple
from time import perf_counter


def get_input(data_file: str) -> Iterable:
    """Read data file and yield lines."""
    with open(data_file) as f:
        for line in f.readlines():
            yield line


def get_bag_info(description: str) -> Tuple:
    """Return tuple with bag name and list of it's children."""
    description = description.replace("bags contain ", ",")
    parent, *children = [x.strip() for x in description.split(",")]
    if children[0].startswith("no other"):
        return parent, None
    all_children = []
    for bag in children:
        number, *rest = bag.split(" ")
        color = " ".join(rest[:-1])
        all_children.append((color, int(number)))
    return parent, all_children


def build_graph(all_bag_descriptions: Iterable) -> Dict:
    """Return graph with all child bags that each parent bag can contain."""
    bags_graph = {}
    for description in all_bag_descriptions:
        parent, children = get_bag_info(description)
        bags_graph[parent] = children
    return bags_graph


def compute_p1(graph: Dict, target: str) -> int:
    """
    Return number of bags that contain target, using Breadth First Search.
    """
    bag_count = 0
    for parent in graph.keys():
        # skip target to prevent counting it twice
        if parent == target:
            continue
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


def compute_p2(graph: Dict, source: str) -> int:
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
    start = perf_counter()
    day7 = get_input("inputs/2020_7.txt")
    day7_graph = build_graph(day7)
    sp1 = perf_counter()
    p1 = compute_p1(day7_graph, "shiny gold")
    sp2 = perf_counter()
    p2 = compute_p2(day7_graph, "shiny gold")
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"constructing graph took {time0}ms and total runtime is {total_time}ms")
