from typing import List


def new_destination(removed: List[str], cur_cup: str) -> str:
    allowed = [str(x) for x in range(1, 10) if str(x) not in removed]
    ind = allowed.index(cur_cup) - 1
    return allowed[ind]


assert new_destination(['8', '9', '1'], '2') == '7'
assert new_destination(['8', '9', '1'], '5') == '4'
assert new_destination(['8', '9', '1'], '7') == '6'
assert new_destination(['3', '2', '1'], '4') == '9'
assert new_destination(['3', '2', '1'], '9') == '8'
assert new_destination(['3', '2', '1'], '5') == '4'


def compute(data: str, moves: int, cups=9):
    cup_order = list(data)
    for move in range(moves):
        print(f'move: {move + 1}')
        print(cup_order)
        position = move % cups
        current_cup = cup_order[position]
        pickup_start = (position + 1) % cups
        pickup_end = (pickup_start + 3) % cups
        if pickup_start < pickup_end:
            picked_up = cup_order[pickup_start: pickup_end]
            circle = cup_order[:pickup_start]
            circle.extend(cup_order[pickup_end:])
        else:
            picked_up = cup_order[pickup_start:]
            picked_up.extend(cup_order[:pickup_end])
            circle = cup_order[pickup_end: pickup_start]
        print(f"picked_up: {picked_up}")
        print(f"circle: {circle}")
        destination_cup = new_destination(picked_up, current_cup)
        print(f"current cup: {current_cup}  destination_cup: {destination_cup}")
        print()
        insert_index = circle.index(destination_cup) + 1
        new_order = circle[:insert_index]
        right = []
        if insert_index < cups - 3:
            right = circle[insert_index:]
        new_order.extend(picked_up)
        new_order.extend(right)
        cup_order = new_order
    return "end"


t0 = '389125467'  # after 10: 92658374 after 100: 67384529
print(compute(t0, 10))

day_23 = '952438716'


"""
-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7 
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7 
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1 
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6 
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1 
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7 
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6 
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5 
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6 
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6"""