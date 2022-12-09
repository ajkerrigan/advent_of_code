import sys
from operator import attrgetter

from coordinates import Direction, Point


def parse_instructions(data: str) -> list:
    instructions = []
    for line in data.splitlines():
        dir, num = line.split()
        instructions.extend(getattr(Direction, dir).value for _ in range(int(num)))
    return instructions


def print_visits(visited):
    xattr = attrgetter("x")
    yattr = attrgetter("y")
    xbound, ybound = (
        (min(visited, key=xattr).x - 2, max(visited, key=xattr).x + 2),
        (min(visited, key=yattr).y - 2, max(visited, key=yattr).y + 2),
    )
    for y in range(*ybound):
        for x in range(*xbound):
            p = Point(x, y)
            print("S" if p == Point(0, 0) else "#" if p in visited else "-", end="")
        print()


def part1(data: str) -> int:
    instructions = parse_instructions(data)
    head, tail = Point(0, 0), Point(0, 0)
    visited = set()

    for inst in instructions:
        head += inst
        tail = tail.close_gap(head)
        visited.add(tail)

    print_visits(visited)
    return len(visited)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
