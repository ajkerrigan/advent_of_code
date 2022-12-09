import sys


def build_grid(data) -> dict:
    """Build a dict of coordinates to values.

    I _think_ I dig this more than a 2-dimensional list.
    """
    grid = {}
    for i, row in enumerate(data.strip().splitlines()):
        for j, col in enumerate(row):
            grid[(i, j)] = int(col)
    return grid


def print_visible(grid, visible):
    """Mental helper to visualize the trees we can see."""
    size = int(len(grid) ** (1 / 2))
    for i in range(size):
        for j in range(size):
            if (i, j) in visible:
                print(grid[(i, j)], end="")
            else:
                print("-", end="")
        print()


def count_visible(grid) -> set:
    size = int(len(grid) ** (1 / 2))
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


def find_view_distance(grid, coord, step):
    val = grid[coord]
    distance = 0
    x, y = coord
    dx, dy = step

    while True:
        x += dx
        y += dy
        new_val = grid.get((x, y))
        if new_val is None:
            # We've hit the edge of the map, son
            break
        distance += 1
        if new_val >= val:
            # That there's a tree
            break
    return distance


def get_view_score(grid, coord):
    views = [
        find_view_distance(grid, coord, step)
        for step in ((0, 1), (0, -1), (1, 0), (-1, 0))
    ]
    view_score = views[0] * views[1] * views[2] * views[3]
    return view_score


def part1(data: str) -> int:
    grid = build_grid(data)
    visible = count_visible(grid)
    print_visible(grid, visible)
    return len(visible)


def part2(data: str) -> int:
    grid = build_grid(data)
    best_view = max(get_view_score(grid, coord) for coord in grid)
    return best_view


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
