import sys
from dataclasses import dataclass
from enum import Enum
from operator import attrgetter


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def close_gap(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        if abs(dx) <= 1 and abs(dy) <= 1:
            return self
        if abs(dx) > 0 and abs(dy) > 0:
            return Point(self.x + (1 if dx > 0 else -1), self.y + (1 if dy > 0 else -1))
        elif abs(dx) > 1:
            return Point(self.x + (1 if dx > 0 else -1), self.y)
        elif abs(dy) > 1:
            return Point(self.x, self.y + (1 if dy > 0 else -1))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Direction(Enum):
    R = Point(1, 0)
    L = Point(-1, 0)
    U = Point(0, -1)
    D = Point(0, 1)


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
