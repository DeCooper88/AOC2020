import AOC20_07

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

t0_graph = AOC20_07.build_graph(t0)
t1_graph = AOC20_07.build_graph(t1)


def test_compute_p1():
    assert AOC20_07.compute_p1(t0_graph, "shiny gold") == 4


def test_compute_p2a():
    assert AOC20_07.compute_p2(t0_graph, "shiny gold") == 32


def test_compute_p2b():
    assert AOC20_07.compute_p2(t1_graph, "shiny gold") == 126
