from collections import deque
from typing import Dict, Deque, List, Set, Tuple, Union
from time import perf_counter


def get_input(data_file: str) -> List[int]:
    with open(data_file) as f:
        return [int(x) for x in f.readlines()]


def compute_p1(data: List[int]) -> int:
    """Answer part 1"""
    adapters = sorted(data)
    device = adapters[-1] + 3
    adapters.append(device)
    cur_jolts = 0
    diffs = []
    for adap in adapters:
        diff = adap - cur_jolts
        diffs.append(diff)
        cur_jolts = adap
    ones = diffs.count(1)
    threes = diffs.count(3)
    return ones * threes


def build_graph(data: List) -> Dict:
    adapters = sorted(data)
    children: Dict[int, Union[List, str]] = {}
    op = [x for x in adapters if x < 4]
    children[0] = op
    for i, dad in enumerate(adapters):
        kids = []
        for kid in adapters[i:]:
            if dad == kid:
                continue
            diff = kid - dad
            if diff < 4:
                kids.append(kid)
        children[dad] = kids
    children[adapters[-1]] = "goal"
    return children


def compute_two(data: List[int]) -> Union[int, str]:
    """
    Very slow algorithm for part 2. Works on the small test inputs,
    but will take years to find answer for actual input.
    """
    start = perf_counter()
    adapters = sorted(data)
    graph = build_graph(adapters)
    frontier: Deque[List[int]] = deque()
    frontier.append([0])
    seen = set()
    routes = 0
    while frontier:
        cur_route = frontier.pop()
        # dad = frontier.pop()
        dad = cur_route[-1]
        kids = graph[dad]
        if kids == "goal":
            routes += 1
            if routes == 1000000:
                end = perf_counter()
                secs = round(end - start, 2)
                msg = f"It took {secs} seconds to find {routes} routes!!\n"
                msg2 = f"there are still {len(frontier)} items left in the queue\n"
                return msg + msg2 + "maybe it's better to stop...."
        else:
            for kid in kids:
                new_route = cur_route + [kid]
                nr_tup: Tuple = tuple(new_route)
                if nr_tup not in seen:
                    frontier.append(new_route)
                    seen.add(nr_tup)
    return routes


def compute_new(data: List[int]) -> int:
    """
    Return possible number of adapter combinations (routes) to get from
    charging outlet (source) to device. The algorithm uses Breadth First
    Search and for every adapter keeps track of the number of routes that
    are possible to get to it.
    Example : [0, 1, 4, 5, 6, 7, 10]
    0 is the source
    1 it is only possible to get to it from 0, so 1 route
    4 it is only possible to get to it from 1, so 1 route
    5 it is only possible to get to it from 4, so 1 route
    6 it is possible to get here from 4 or 5, so 2 routes
    """
    adapters = sorted(data)
    graph = build_graph(adapters)
    frontier: Deque[int] = deque()
    frontier.append(0)
    seen = {0: 1}
    all_dads: Dict[int, Set[int]] = {0: set()}
    routes = 0
    while frontier:
        dad = frontier.popleft()
        kids = graph[dad]
        if kids == "goal":
            continue
        for kid in kids:
            if kid not in all_dads:
                all_dads[kid] = set()
            all_dads[kid].add(dad)
            if kid not in seen:
                frontier.append(kid)
                seen[kid] = seen[dad]
            else:
                r = 0  # r is sum of all routes of all dads
                for daddy in all_dads[kid]:
                    r += seen[daddy]
                seen[kid] = r
                routes = max(routes, r)
    return routes


def compute_p2(data: List[int]) -> int:
    """Dynamic programming solution part two."""
    arrangements = {}
    adapters = [0] + sorted(data)
    arrangements[adapters[0]] = 1
    arrangements[adapters[1]] = 1
    for i, a in enumerate(adapters[2:], start=2):
        previous = adapters[max(i - 3, 0) : i]
        sources = 0
        for p in previous:
            if a - p < 4:
                sources += arrangements[p]
        arrangements[a] = sources
    return arrangements[adapters[-1]]


if __name__ == "__main__":
    t0 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    t1 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
          38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]

    assert compute_p1(t0) == 35
    assert compute_p1(t1) == 220
    assert compute_p2(t0) == 8
    assert compute_p2(t1) == 19208

    start = perf_counter()
    day10 = get_input("inputs/2020_10.txt")
    sp1 = perf_counter()
    p1 = compute_p1(day10)
    sp2 = perf_counter()
    p2 = compute_p2(day10)
    end = perf_counter()
    time0 = round((sp1 - start) * 1000, 3)
    time1 = round((sp2 - sp1) * 1000, 3)
    time2 = round((end - sp2) * 1000, 3)
    total_time = round((end - start) * 1000, 3)
    print(f"solution part 1: {p1} ({time1}ms)")
    print(f"solution part 2: {p2} ({time2}ms)")
    print(f"data import took {time0}ms and total runtime is {total_time}ms\n")
