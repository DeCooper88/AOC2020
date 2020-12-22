from helpers import file_reader
from collections import deque
from time import perf_counter


def compute(data: str) -> int:
    """
    Play a game of space cards. Return winning player's score, which is
    solution part 1.
    """
    p1_raw, p2_raw = data.strip().split("\n\n")
    hand1 = deque(
        [
            int(card)
            for card in p1_raw.strip().split("\n")
            if not card.startswith("Play")
        ]
    )
    hand2 = deque(
        [
            int(card)
            for card in p2_raw.strip().split("\n")
            if not card.startswith("Play")
        ]
    )
    while True:
        p1 = hand1.popleft()
        p2 = hand2.popleft()
        if p1 > p2:
            hand1.extend([p1, p2])
            last_winner = "p1"
        else:
            hand2.extend([p2, p1])
            last_winner = "p2"
        winner = len(hand1) == 0 or len(hand2) == 0
        if winner:
            break
    winning_hand = hand1 if last_winner == "p1" else hand2
    card_count = len(winning_hand)
    points = [card * (card_count - i) for i, card in enumerate(winning_hand)]
    return sum(points)


if __name__ == '__main__':
    t0 = file_reader('examples/AOC20_22_example.txt')
    assert compute(t0) == 306

    start = perf_counter()
    day22 = file_reader("inputs/2020_22.txt")
    part1 = compute(day22)
    end = perf_counter()
    runtime = round((end - start) * 1000, 1)
    print(f"solution part 1: {part1}")
    print(f"runtime: {runtime}ms")
