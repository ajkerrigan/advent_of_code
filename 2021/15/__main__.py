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


def shortest_path(grid):
    shortest_grid = {(0, 0): 0}
    size = int(len(grid) ** (1 / 2))
    end = (size - 1, size - 1)
    while len(shortest_grid) < len(grid):
        for point, risk in sorted(grid.items(), key=lambda i: sum(i[0])):
            possible_risk = [
                shortest_grid[p[0]]
                for p in get_neighbors(grid, point)
                if p[0] in shortest_grid
            ]
            if possible_risk:
                shortest_grid[point] = min(possible_risk) + risk
    return shortest_grid[end]


def repeat_grid(grid, n):
    original_size = int(len(grid) ** (1 / 2))
    risk_scores = tuple(range(1, 10))
    grid = {
        (original_size * i + k[0], k[1]): risk_scores[(v + i) % 9 - 1]
        for k, v in grid.items()
        for i in range(n)
    }

    return {
        (k[0], original_size * i + k[1]): risk_scores[(v + i) % 9 - 1]
        for k, v in grid.items()
        for i in range(n)
    }


def visualize_grid(grid, chunklines=None):
    size = int(len(grid) ** (1 / 2))
    return "\n".join(
        "".join(
            str(grid[(x, y)])
            + ("\n" if chunklines and (x + 1) % chunklines == 0 else "")
            for x in range(size)
        )
        for y in range(size)
    )


if __name__ == "__main__":
    grid = populate_grid(sys.stdin)
    print(f"Part 1: {shortest_path(grid)}")
    part2_grid = repeat_grid(grid, 5)
    print(f"Part 2: {shortest_path(part2_grid)}")
