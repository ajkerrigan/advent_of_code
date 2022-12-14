import logging
import os
import sys
from itertools import pairwise

logging.basicConfig(
    level=logging.DEBUG if os.environ.get("AOC_VERBOSE") else logging.WARNING
)


def get_path(src, dest):
    (x1, x2), (y1, y2) = (sorted(coord) for coord in zip(src, dest))
    path = {}
    for i in range(x1, x2 + 1):
        path[i, y1] = "#"
    for i in range(y1, y2 + 1):
        path[x1, i] = "#"
    return path


def build_grid(data):
    grid = {}

    for line in data.splitlines():
        for ends in pairwise(line.split(" -> ")):
            grid.update(get_path(*(map(int, end.split(",")) for end in ends)))

    grid[500, 0] = "+"
    return grid


def print_grid(grid):
    log = logging.getLogger("print_grid")
    (xmin, xmax), (ymin, ymax) = ((min(pos), max(pos) + 1) for pos in zip(*grid))
    for y in range(ymin, ymax):
        log.debug("".join(grid.get((x, y), ".") for x in range(xmin, xmax)))


def part1(data: str) -> int:
    grid = build_grid(data)
    if os.environ.get("AOC_VERBOSE") in ("part1", "both"):
        print_grid(grid)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
