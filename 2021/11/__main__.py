import sys
from dataclasses import dataclass
from itertools import count


@dataclass
class Octopus:
    x: int
    y: int
    energy: int
    flashed: bool = False

    def __hash__(self):
        return hash((self.x, self.y))


def populate_grid(data):
    """Build a grid of tightly packed octopuses"""
    return {
        (x, y): Octopus(x, y, energy=int(col))
        for y, row in enumerate(data)
        for x, col in enumerate(row)
    }


def get_neighbors(grid, octo):
    """Helper to get adjacent octopuses"""
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
            neighbor.energy > 9 and not (
                neighbor.flashed or neighbor in flashers
            ) and new_flashers.add(neighbor)
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


def part1(data):
    grid = populate_grid(data)
    flashes = 0
    for i in range(100):
        flashes += len(step(grid))
    return flashes


def part2(data):
    grid = populate_grid(data)
    for i in count(1):
        if len(step(grid)) == len(grid):
            return i


if __name__ == "__main__":
    data = [line.strip() for line in sys.stdin.readlines()]
    print(f"Part 1 answer: {part1(data)}")
    print(f"Part 2 answer: {part2(data)}")
