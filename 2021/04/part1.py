from functools import lru_cache


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


def play_bingo(drawn_numbers, boards):
    win = None
    for number in drawn_numbers:
        if win:
            break
        for i, board in enumerate(boards):
            if pos := board.numbers.get(number):
                board.marked.add(pos)
                win = [w for w in get_winning_positions(pos) if w <= board.marked]
                if win:
                    unmarked = (
                        int(k)
                        for k, v in board.numbers.items()
                        if v not in board.marked
                    )
                    print(f"Part 1 answer: {sum(unmarked) * int(number)}")
                    break
