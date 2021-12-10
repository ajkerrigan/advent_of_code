import operator
import sys
from functools import reduce


def populate_grid(data):
    return {
        (x, y): int(col)
        for y, row in enumerate(data)
        for x, col in enumerate(row.strip())
    }


def get_neighbors(point):
    x, y = point
    return ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))


def find_low_points(grid):
    return {
        k: v
        for k, v in grid.items()
        if v < min(grid.get(adj, 9) for adj in get_neighbors(k))
    }


def find_low_neighbors(grid, point, value):
    return {point} | {
        low_neighbor
        for neighbor_k in get_neighbors(point)
        if value < (neighbor_v := grid.get(neighbor_k, 9)) < 9
        for low_neighbor in find_low_neighbors(grid, neighbor_k, neighbor_v)
    }


def find_basin_sizes(grid, low_points):
    return [len(find_low_neighbors(grid, k, v)) for k, v in low_points.items()]


if __name__ == "__main__":
    grid = populate_grid(sys.stdin)
    low_points = find_low_points(grid)
    basin_sizes = find_basin_sizes(grid, low_points)
    print(f"Part 1: {sum(x + 1 for x in low_points.values())}")
    print(f"Part 2: {reduce(operator.mul, sorted(basin_sizes)[-3:])}")
