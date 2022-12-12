import sys
from coordinates import Square, Direction, Mark


def build_grid(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, square in enumerate(line):
            grid[(x, y)] = Square(x, y, square, getattr(Mark, square, None))
    return grid


def print_grid(grid):
    xmax, ymax = (val + 1 for val in max(grid))
    for y in range(ymax):
        print("".join(str(grid[x, y]) for x in range(xmax)))


def part1(data: str) -> int:
    grid = build_grid(data)
    print_grid(grid)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
