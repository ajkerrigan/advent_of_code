from dataclasses import dataclass
from enum import Enum
from string import ascii_lowercase

ELEVATIONS = {**{v: k for k, v in enumerate(ascii_lowercase)}, "S": 0, "E": 25}


@dataclass
class Square:
    x: int
    y: int
    mark: str = ""

    @property
    def coords(self):
        return (self.x, self.y)

    @property
    def elevation(self):
        return ELEVATIONS.get(self.mark, 0)

    def __add__(self, other):
        return Square(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Square(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return self.elevation


class Direction(Enum):
    R = Square(1, 0)
    L = Square(-1, 0)
    U = Square(0, -1)
    D = Square(0, 1)
