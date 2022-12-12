import os
import sys

from coordinates import Direction, Square


def build_grid(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, square in enumerate(line):
            grid[(x, y)] = Square(x, y, square)
    return grid


def print_grid(grid):
    xmax, ymax = (val + 1 for val in max(grid))
    for y in range(ymax):
        print("".join(grid[x, y].mark for x in range(xmax)))


def find_shortest_path(grid, paths):
    visited = {p[0] for p in paths}
    while True:
        new_paths = []
        # Start with the shortest path so if multiple paths converge
        # on the same spot, the shortest one gets there first
        for path in sorted(paths, key=len):
            last_step = path[-1]
            next_steps = [
                grid.get((last_step + direction.value).coords)
                for direction in Direction
            ]
            for step in next_steps:
                if not step:
                    # We're off the grid
                    continue
                if step.elevation > (last_step.elevation + 1):
                    # Too steep, can't go this way
                    continue
                if step in visited:
                    # Already been here, revisiting can't be shortest
                    continue
                new_paths.append(path + [step])
                visited.add(step)
                if step.mark == 'E':
                    # o/~ Looks like we maaaaaade it o/~
                    return len(path)
        paths = new_paths


def part1(grid: dict) -> int:
    grid = build_grid(data)
    # The journey starts with a single step
    paths = [[point] for point in grid.values() if point.mark == 'S']
    return find_shortest_path(grid, paths)


def part2(grid: dict) -> int:
    grid = build_grid(data)
    # The journey starts with a single step
    paths = [[point] for point in grid.values() if point.elevation == 0]
    return find_shortest_path(grid, paths)


if __name__ == "__main__":
    data = sys.stdin.read()
    grid = build_grid(data)
    if os.environ.get("AOC_VERBOSE"):
        print_grid(grid)
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
