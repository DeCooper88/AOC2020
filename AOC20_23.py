from typing import List
from time import perf_counter


def new_destination(removed: List[str], cur_cup: str) -> str:
    """Return new destination. Helper function part 1."""
    allowed = [str(x) for x in range(1, 10) if str(x) not in removed]
    ind = allowed.index(cur_cup) - 1
    return allowed[ind]


def compute(data: str, rounds: int, cups=9) -> str:
    """
    Play a number of rounds of the crab game. Return the labels on
    the cups after cup 1.
    """
    cup_order = list(data)
    current_cup = cup_order[0]
    for move in range(rounds):
        current_cup_index = cup_order.index(current_cup)
        pickup_start = (current_cup_index + 1) % cups
        pickup_end = (pickup_start + 3) % cups
        if pickup_start < pickup_end:
            picked_up = cup_order[pickup_start:pickup_end]
            circle = cup_order[:pickup_start]
            circle.extend(cup_order[pickup_end:])
        else:
            picked_up = cup_order[pickup_start:]
            picked_up.extend(cup_order[:pickup_end])
            circle = cup_order[pickup_end:pickup_start]
        destination_cup = new_destination(picked_up, current_cup)
        insert_index = circle.index(destination_cup) + 1
        new_order = circle[:insert_index]
        right = []
        if insert_index < cups - 3:
            right = circle[insert_index:]
        new_order.extend(picked_up)
        new_order.extend(right)
        cup_order = new_order
        new_index_cur_cup = cup_order.index(current_cup)
        current_cup = cup_order[(new_index_cur_cup + 1) % cups]
    uno_index = cup_order.index("1")
    if uno_index == cups - 1:
        return "".join(cup_order[cups - 1])
    elif uno_index == 0:
        return "".join(cup_order[1:])
    else:
        left = cup_order[uno_index + 1 :]
        right = cup_order[:uno_index]
    return "".join(left + right)


if __name__ == "__main__":
    assert new_destination(["8", "9", "1"], "2") == "7"
    assert new_destination(["8", "9", "1"], "5") == "4"
    assert new_destination(["8", "9", "1"], "7") == "6"
    assert new_destination(["3", "2", "1"], "4") == "9"
    assert new_destination(["3", "2", "1"], "9") == "8"
    assert new_destination(["3", "2", "1"], "5") == "4"

    assert compute("389125467", 10) == "92658374"
    assert compute("389125467", 100) == "67384529"

    start = perf_counter()
    day_23 = "952438716"
    p1 = compute(day_23, 100)
    end = perf_counter()
    runtime = round((end - start) * 1000, 1)
    print(f"solution part 1: {p1}")
    print(f"runtime: {runtime}ms")
