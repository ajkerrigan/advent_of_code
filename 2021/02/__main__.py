from pkg_resources import resource_filename
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Position:
    horizontal: int = 0
    depth: int = 0

    def __add__(self, other):
        return Position(self.horizontal + other.horizontal, self.depth + other.depth)

    def __mul__(self, other):
        return Position(self.horizontal * int(other), self.depth * int(other))

TRANSITIONS = {
    'forward': Position(1, 0),
    'down': Position(0, 1),
    'up': Position(0, -1),
}

print('Part 1...')
with open(Path(resource_filename(__name__, "input"))) as f:
    end = Position(0, 0)
    for line in f:
        direction, magnitude = line.split()
        end += TRANSITIONS[direction] * magnitude

    print(f'Final position: {end}')
    print(f'Product of coordinates: {end.horizontal * end.depth}')
