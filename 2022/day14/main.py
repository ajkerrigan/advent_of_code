import logging
import os
import sys
from itertools import pairwise
from enum import StrEnum

logging.basicConfig(
    level=logging.DEBUG if os.environ.get("AOC_VERBOSE") else logging.WARNING
)

SOURCE_COORDS = (500, 0)


class Mark(StrEnum):
    FALLING_SAND = "X"
    RESTING_SAND = "o"
    PATH = "#"
    AIR = "."
    SAND_SOURCE = "+"


def get_path(src, dest):
    (x1, x2), (y1, y2) = (sorted(coord) for coord in zip(src, dest))
    path = {}
    for i in range(x1, x2 + 1):
        path[i, y1] = Mark.PATH
    for i in range(y1, y2 + 1):
        path[x1, i] = Mark.PATH
    return path


def build_grid(data):
    grid = {}

    for line in data.splitlines():
        for ends in pairwise(line.split(" -> ")):
            grid.update(get_path(*(map(int, end.split(",")) for end in ends)))

    grid[SOURCE_COORDS] = Mark.SAND_SOURCE
    return grid


def print_grid(grid):
    log = logging.getLogger("print_grid")
    (xmin, xmax), (ymin, ymax) = ((min(pos), max(pos) + 1) for pos in zip(*grid))
    for y in range(ymin, ymax):
        log.debug("".join(grid.get((x, y), ".") for x in range(xmin, xmax)))


def void_bound(grid, x, y):
    stoppers = [
        pos
        for pos in grid
        if pos[0] == x and pos[1] >= y and grid[pos] != Mark.FALLING_SAND
    ]
    return not stoppers


def find_resting_spot(grid, x, y):
    for coord in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1)):
        rest = grid.get(coord, Mark.AIR)
        if rest == Mark.AIR:
            return coord
    return x, y


def drop_sand(grid, position):
    x, y = position
    while True:
        rest = find_resting_spot(grid, x, y)
        grid[rest] = Mark.FALLING_SAND
        if os.environ.get("AOC_VERBOSE") in ("part1", "both"):
            print_grid(grid)
        if void_bound(grid, *rest):
            return grid, False
        if rest == (x, y):
            grid[rest] = Mark.RESTING_SAND
            break
        else:
            del grid[rest]
        x, y = rest
    return grid, True


def part1(data: str) -> int:
    grid = build_grid(data)
    sand_accumulating = True
    while sand_accumulating:
        grid, sand_accumulating = drop_sand(grid, SOURCE_COORDS)
    if os.environ.get("AOC_VERBOSE") in ("part1", "both"):
        print_grid(grid)
    return sum(mark == Mark.RESTING_SAND for mark in grid.values())


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
