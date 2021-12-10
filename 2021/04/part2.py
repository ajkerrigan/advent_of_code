from part1 import get_winning_positions


def play_bingo(drawn_numbers, boards):
    done = False
    for number in drawn_numbers:
        if done:
            break
        for i, board in enumerate(boards):
            if pos := board.numbers.get(number):
                board.marked.add(pos)
                win = [w for w in get_winning_positions(pos) if w <= board.marked]
                if win:
                    board.winner = True
                    if all(b.winner for b in boards):
                        unmarked = (
                            int(k)
                            for k, v in board.numbers.items()
                            if v not in board.marked
                        )
                        print(f"Part 2 answer: {sum(unmarked) * int(number)}")
                        done = True
                        break
