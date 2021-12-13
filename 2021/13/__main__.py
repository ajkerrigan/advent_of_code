import sys


def populate_sparse_grid(data):
    grid = {}
    fold_text = "fold along "
    xbound, ybound = 0, 0
    for line in data:
        if "," in line:
            x, y = (int(i) for i in line.split(","))
            grid[(x, y)] = True
            xbound = max((xbound, x))
            ybound = max((ybound, y))
        elif fold_text in line:
            axis, pos = line.strip(fold_text).split("=")
            grid.setdefault("folds", []).append((axis, int(pos)))
    grid["bounds"] = (xbound, ybound)
    return grid


def visualize_grid(grid):
    return "\n".join(
        "".join("#" if grid.get((x, y)) else "." for x in range(grid["bounds"][0]))
        for y in range(grid["bounds"][1])
    )


def fold_grid(grid, axis, pos):
    new_grid = {}
    xbound = axis == "x" and pos or grid["bounds"][0]
    ybound = axis == "y" and pos or grid["bounds"][1]
    for y in range(ybound + 1):
        for x in range(xbound + 1):
            new_grid[(x, y)] = grid.get((x, y)) or grid.get(
                (
                    (pos * 2 - x) if axis == "x" else x,
                    (pos * 2 - y) if axis == "y" else y,
                )
            )
    new_grid["bounds"] = (xbound, ybound)
    return new_grid


def part1(grid):
    axis, pos = grid.get("folds", ())[0]
    grid = fold_grid(grid, axis, pos)
    return len([k for k, v in grid.items() if v and isinstance(k, tuple)])


def part2(grid):
    for fold in grid.get("folds", ()):
        axis, pos = fold
        grid = fold_grid(grid, axis, pos)
    return grid


if __name__ == "__main__":
    data = sys.stdin.readlines()
    grid = populate_sparse_grid(data)
    print(f"Part 1: {part1(grid)}")

    print("\n".join(["Part 2:", visualize_grid(part2(grid))]))
