import sys
from dataclasses import dataclass, field

data = [line.strip() for line in sys.stdin.readlines()]


@dataclass
class Octopus:
    x: int
    y: int
    energy: int
    flashed: bool = False

    def __hash__(self):
        return hash((self.x, self.y))

def populate_grid(data):
    """Build a heightmap grid mapping (x,y) coordinates to height"""
    return {(x, y): Octopus(x, y, energy=int(col)) for y, row in enumerate(data) for x, col in enumerate(row)}


grid = populate_grid(data)

def get_neighbors(grid, octo):
    """Helper to get neighbor coordinates for a given point

    Note: These coordinates are not guaranteed to exist on
    the grid
    """
    return (
        grid[n]
        for n in (
            (octo.x, octo.y - 1),
            (octo.x, octo.y + 1),
            (octo.x - 1, octo.y),
            (octo.x + 1, octo.y),
            (octo.x - 1, octo.y - 1),
            (octo.x + 1, octo.y + 1),
            (octo.x - 1, octo.y + 1),
            (octo.x + 1, octo.y - 1),
        )
        if n in grid
    )


def flash(grid, flashers):
    new_flashers = set()
    for octo in flashers:
        octo.flashed = True
        for neighbor in get_neighbors(grid, octo):
            neighbor.energy += 1
            neighbor.energy > 9 and not (neighbor.flashed or neighbor in flashers) and new_flashers.add(neighbor)
    return flashers | (new_flashers and flash(grid, new_flashers))


def step(grid):
    flashers = set()
    for octo in grid.values():
        octo.energy += 1
        octo.energy > 9 and flashers.add(octo)
    flashed = flash(grid, flashers)
    for octo in flashed:
        octo.energy = 0
        octo.flashed = False
    return flashed

def print_grid(grid):
    for y in range(10):
        for x in range(10):
            print(grid[(x, y)].energy, end='')
        print()
flashes = 0
for i in range(100):
    flashes += len(step(grid))
    if i % 1 == 0:
        print(f'step: {i}')
        print_grid(grid)
print(flashes)
