import sys


def populate_grid(data):
    return {
        (x, y): int(col)
        for y, row in enumerate(data)
        for x, col in enumerate(row.strip())
    }


def get_neighbors(grid, point):
    def _get_neighbors(point):
        x, y = point
        return (
            (k, grid[k])
            for k in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1))
            if k in grid
        )

    return _get_neighbors(point)


if __name__ == "__main__":
    grid = populate_grid(sys.stdin)
    shortest_grid = {(0, 0): 0}
    size = int(len(grid) ** (1 / 2))
    end = (size - 1, size - 1)
    while True:
        for point, risk in grid.items():
            possible_risk = [
                shortest_grid.get(p[0])
                for p in get_neighbors(grid, point)
                if p[0] in shortest_grid
            ]
            if possible_risk:
                shortest_grid[point] = min(possible_risk) + risk
        if len(grid) == len(shortest_grid):
            break
    print(shortest_grid[end])
