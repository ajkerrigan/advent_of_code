import logging
import re
import sys
from copy import deepcopy


def build_initial_position(starting_stacks):
    stacks = {}
    for level in starting_stacks[-2::-1]:
        for i, crate in enumerate(level[1::4]):
            if crate == " ":
                continue
            stacks.setdefault(i, []).append(crate)
    return stacks


def move_crates(stacks, moves, model9000=True):
    new_stacks = deepcopy(stacks)
    for move in moves:
        num_crates, move_from, move_to = (int(n) for n in re.findall(r"\d+", move))
        stay, go = (
            new_stacks[move_from - 1][:-num_crates],
            new_stacks[move_from - 1][-num_crates:],
        )
        new_stacks[move_from - 1] = stay
        new_stacks[move_to - 1].extend(reversed(go) if model9000 else go)
    return new_stacks


def part1(stacks, moves):
    final_position = move_crates(stacks, moves)
    return "".join(stack[-1] for stack in final_position.values())


def part2(stacks, moves):
    final_position = move_crates(stacks, moves, model9000=False)
    return "".join(stack[-1] for stack in final_position.values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    starting_stacks, moves = (x.splitlines() for x in data.split("\n\n"))
    stacks = build_initial_position(starting_stacks)
    print(f"Part 1: {part1(stacks, moves)}")
    print(f"Part 2: {part2(stacks, moves)}")
