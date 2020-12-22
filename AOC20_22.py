from helpers import file_reader
from collections import deque


def compute(data: str) -> int:
    p1_raw, p2_raw = data.strip().split('\n\n')
    hand1 = deque([int(card) for card in p1_raw.strip().split('\n') if not card.startswith('Play')])
    hand2 = deque([int(card) for card in p2_raw.strip().split('\n') if not card.startswith('Play')])
    card_counts = len(hand1) * 2
    rounds = 0
    while True:
        p1 = hand1.popleft()
        p2 = hand2.popleft()
        if p1 > p2:
            hand1.extend([p1, p2])
            last_winner = 'p1'
        else:
            hand2.extend([p2, p1])
            last_winner = 'p2'
        rounds += 1
        winner = len(hand1) == 0 or len(hand2) == 0
        if winner:
            break
    # TODO: assumes player 2 wins, needs fix
    points = [card * (card_counts - i) for i, card in enumerate(hand2, start=0)]
    # print("rounds played:", rounds)
    # print(points)
    return sum(points)


t0 = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


assert compute(t0) == 306

day22 = file_reader('inputs/2020_22.txt')
print(compute(day22))
