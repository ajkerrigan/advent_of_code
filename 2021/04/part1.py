import sys
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import islice

drawn_numbers = next(sys.stdin).split(",")


@dataclass
class Board:
    numbers: dict = field(default_factory=dict)
    marked: set = field(default_factory=set)


boards: list[Board] = []

for line in sys.stdin:
    if line.strip() == "":
        board = Board()
        for row, board_numbers in enumerate(islice(sys.stdin, 5)):
            for col, num in enumerate(board_numbers.split(), start=0):
                board.numbers[num] = (row, col)
        boards.append(board)


@lru_cache
def get_winning_positions(pos):
    row, col = pos
    return [
        # vertical
        {((row + i) % 5, col) for i in range(5)},
        # horizontal
        {(row, (col + i) % 5) for i in range(5)},
        # maybe diagonals too
        *(
            ({(i, i) for i in range(5)}, {(5 - i, i) for i in range(5)})
            if abs(row) == abs(col)
            else ()
        ),
    ]


win = None
for number in drawn_numbers:
    if win:
        break
    for i, board in enumerate(boards):
        if pos := board.numbers.get(number):
            board.marked.add(pos)
            win = [w for w in get_winning_positions(pos) if w <= board.marked]
            if win:
                print(f"we have a winner! number {number} on board {i}!")
                print(f"win: {sorted(win[0])}")
                unmarked = (
                    int(k) for k, v in board.numbers.items() if v not in board.marked
                )
                print(f"Part 1 answer: {sum(unmarked) * int(number)}")
                break
