import sys


def populate_grid(data):
    """Build a heightmap grid mapping (x,y) coordinates to height"""
    return {
        (x, y): int(col)
        for y, row in enumerate(data)
        for x, col in enumerate(row.strip())
    }

def get_neighbors(grid, point):
    def _get_neighbors(point):
        x, y = point
        return sorted(
            ((k, grid[k])
            for k in
            (
                (x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)
            )
            if k in grid),
            key=lambda x: (x[1], -(x[0][0]), -(x[0][1]))
        )
    return _get_neighbors(point)


if __name__ == '__main__':
    grid = populate_grid(sys.stdin)
    shortest_grid = {(0, 0): 0}
    size = int(len(grid) ** (1/2))
    end = (size-1, size-1)
    while True:
        for point, risk in shortest_grid.copy().items():
            for n in (n for n in get_neighbors(grid, point) if n[0] not in shortest_grid):
                possible_risk = (shortest_grid.get(p[0], 1_000_000) for p in get_neighbors(grid, n[0]))
                shortest_grid[n[0]] = n[1] + min(possible_risk)
        if len(grid) == len(shortest_grid):
            break
    print(shortest_grid[end])
