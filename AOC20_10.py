from helpers import file_reader
from collections import deque, Counter


def compute(data):
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
    print(diffs)
    # print(ones, threes)
    return ones * threes


def compute_one_all(data):
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
    twos = diffs.count(2)
    threes = diffs.count(3)
    print(ones, twos, threes)
    return ones ** threes


def successors(data):
    adapters = sorted(data)
    device = adapters[-1] + 3
    # adapters.append(device)
    children = {}
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
            else:
                break
        children[dad] = kids
    children[adapters[-1]] = "goal"
    # children[adapters[-1]] = []
    return children


def compute_two(data):
    adapters = sorted(data)
    graph = successors(adapters)
    frontier = deque()
    frontier.append([0])
    seen = set()
    routes = 0
    while frontier:
        cur_route = frontier.pop()
        # print(cur_route)
        dad = cur_route[-1]
        kids = graph[dad]
        if kids == 'goal':
            # print(list(reversed(cur_route)))
            # print('found goal, count =', routes)
            routes += 1
        else:
            for kid in kids:
                new_route = cur_route + [kid]
                nr_tup = tuple(new_route)
                if nr_tup not in seen:
                    frontier.append(new_route)
                    seen.add(nr_tup)
    # print(adapters)
    # print(graph)
    return routes


def compute_new(data):
    adapters = sorted(data)
    graph = successors(adapters)
    frontier = deque()
    frontier.append(0)
    seen = {0: 1}  # value needs to be sum routes of all dads of key
    all_dads = {0: set()}
    # seen[0] = 1
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
                r = 0
                for daddy in all_dads[kid]:
                    r += seen[daddy]
                seen[kid] = r
                routes = max(routes, r)
    return routes


t0_raw = """16
10
15
5
1
11
7
19
6
12
4"""

t1_raw = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


t0 = [int(x.strip()) for x in t0_raw.strip().split('\n')]
t1 = [int(x.strip()) for x in t1_raw.strip().split('\n')]
# print(t1)
# print(compute(t0))
# print(compute(t1))
# print(compute_one_all(t0))
# print(compute_one_all(t1))
# print(successors(t0))
# print(compute_two(t0))
# print(compute_two(t1))
print(compute_new(t0))
print(compute_new(t1))


day10_raw = file_reader('inputs/2020_10.txt', output='lines')
day10 = [int(x) for x in day10_raw]
# print(compute(day10))
# print(compute_one_all(day10))
# print(successors(day10))
# print(compute_two(day10))
print(compute_new(day10))
