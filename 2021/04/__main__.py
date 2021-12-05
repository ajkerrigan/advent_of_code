import sys
from dataclasses import dataclass, field
from itertools import islice

import part1
import part2


@dataclass
class Board:
    # Dict mapping a number to its (row, col) position
    numbers: dict = field(default_factory=dict)

    # Set of marked (row, col) positions
    marked: set = field(default_factory=set)

    # Has this board won yet?
    winner: bool = False


drawn_numbers = next(sys.stdin).split(",")
boards: list[Board] = []
for line in sys.stdin:
    if line.strip() == "":
        board = Board()
        for row, board_numbers in enumerate(islice(sys.stdin, 5)):
            for col, num in enumerate(board_numbers.split(), start=0):
                board.numbers[num] = (row, col)
        boards.append(board)

part1.play_bingo(drawn_numbers, boards)
part2.play_bingo(drawn_numbers, boards)
