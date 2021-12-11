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
        """Hash based on position"""
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
    """Flash an octopus

    - Add energy to all neighbors
    - If neighbor energy goes above 9, they flash also
    - Nobody can flash more than once per step
    """
    new_flashers = set()
    for octo in flashers:
        octo.flashed = True
        for neighbor in get_neighbors(grid, octo):
            neighbor.energy += 1
            if neighbor.energy > 9 and not (neighbor.flashed or neighbor in flashers):
                new_flashers.add(neighbor)
    return flashers | (new_flashers and flash(grid, new_flashers))


def step(grid):
    """Run one step of octopus flash dance:

    - Everybody gets a hit of energy
    - Flash if energy > 9
    - Reset all tired flashers to 0

    Return the set of all octopuses who flashed
    during this step.
    """
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
    return sum(len(step(grid)) for _ in range(100))


def part2(data):
    grid = populate_grid(data)
    return next(i for i in count(1) if len(step(grid)) == len(grid))


if __name__ == "__main__":
    data = [line.strip() for line in sys.stdin.readlines()]
    print(f"Part 1 answer: {part1(data)}")
    print(f"Part 2 answer: {part2(data)}")
