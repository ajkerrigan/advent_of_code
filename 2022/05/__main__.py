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


def move_crates(stacks, moves):
    new_stacks = deepcopy(stacks)
    for move in moves:
        num_crates, move_from, move_to = (int(n) for n in re.findall(r"\d+", move))
        for _ in range(num_crates):
            new_stacks[move_to - 1].append(new_stacks[move_from - 1].pop())
    return new_stacks


def part1(data):
    starting_stacks, moves = (x.splitlines() for x in data.split("\n\n"))
    stacks = build_initial_position(starting_stacks)
    final_position = move_crates(stacks, moves)
    return "".join(stack[-1] for stack in final_position.values())


def part2(data):
    ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
