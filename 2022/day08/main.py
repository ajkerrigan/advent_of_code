import sys


def build_grid(data) -> dict:
    grid = {}
    for i, row in enumerate(data.strip().splitlines()):
        for j, col in enumerate(row):
            grid[(i, j)] = int(col)
    grid["size"] = i + 1
    return grid


def print_visible(grid, visible):
    size = grid["size"]
    for i in range(size):
        for j in range(size):
            if (i, j) in visible:
                print(grid[(i, j)], end="")
            else:
                print("-", end="")
        print()


def count_visible(grid) -> set:
    size = grid["size"]
    visible = set()
    for i in range(size):
        # forward and backward
        for r in (range(size), range(size - 1, -1, -1)):
            # loop for row,col and col,row
            high = -1
            for j in r:
                if grid[(i, j)] > high:
                    high = grid[(i, j)]
                    visible.add((i, j))
            visible.add((i, j))
            high = -1
            for j in r:
                if grid[(j, i)] > high:
                    high = grid[(j, i)]
                    visible.add((j, i))
            visible.add((j, i))
    return visible


def part1(data: str) -> int:
    grid = build_grid(data)
    visible = count_visible(grid)
    print_visible(grid, visible)
    return len(visible)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
