import os
import sys
from operator import attrgetter
from itertools import pairwise

from coordinates import Direction, Point


def parse_instructions(data: str) -> list:
    instructions = []
    for line in data.splitlines():
        dir, num = line.split()
        instructions.extend(getattr(Direction, dir).value for _ in range(int(num)))
    return instructions


def print_visits(visited, positions):
    xattr = attrgetter("x")
    yattr = attrgetter("y")
    xbound, ybound = (
        (min(visited, key=xattr).x - 2, max(visited, key=xattr).x + 2),
        (min(visited, key=yattr).y - 2, max(visited, key=yattr).y + 2),
    )
    marks = {pos: str(i) for i, pos in enumerate(positions)}
    marks[Point(0, 0)] = "S"
    for y in range(*ybound):
        for x in range(*xbound):
            p = Point(x, y)
            print("#" if p in visited else marks.get(p, "."), end="")
        print()


def part1(data: str) -> int:
    instructions = parse_instructions(data)
    head, tail = Point(0, 0), Point(0, 0)
    visited = set()

    for inst in instructions:
        head += inst
        tail = tail.close_gap(head)
        visited.add(tail)
    if os.environ.get("AOC_VERBOSE", "").lower() in ("part1", "both"):
        print_visits(visited, [head, tail])
    return len(visited)


def part2(data: str) -> int:
    instructions = parse_instructions(data)
    positions = [Point(0, 0)] * 10
    visited = set()

    for inst in instructions:
        positions[0] += inst
        positions = [
            positions[0],
            *(p2.close_gap(p1) for p1, p2 in pairwise(positions)),
        ]
        visited.add(positions[-1])
    if os.environ.get("AOC_VERBOSE", "").lower() in ("part2", "both"):
        print_visits(visited, positions)
    return len(visited)


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
