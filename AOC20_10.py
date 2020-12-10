from helpers import file_reader
from collections import deque
from typing import Dict, Deque, List, Set, Tuple, Union
from time import perf_counter


def compute(data: List[int]) -> int:
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
        if kids == 'goal':
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
        if kids == 'goal':
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


if __name__ == '__main__':
    t0 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    t1 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
          38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]

    assert compute(t0) == 35
    assert compute(t1) == 220
    assert compute_new(t0) == 8
    assert compute_new(t1) == 19208
    assert compute_two(t0) == 8
    assert compute_two(t1) == 19208

    day10_raw = file_reader('inputs/2020_10.txt', output='lines')
    day10 = [int(x) for x in day10_raw]

    st = perf_counter()
    p1 = compute(day10)
    p2 = compute_new(day10)
    end = perf_counter()
    tot_time = round((end - st) * 1000, 1)
    print(f"solution part 1: {p1}")
    print(f"solution part 2: {p2}")
    print(f"execution time: {tot_time}ms")

    # print(compute_two(day10))
