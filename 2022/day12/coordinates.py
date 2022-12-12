from dataclasses import dataclass
from enum import Enum, Flag, auto
from string import ascii_lowercase

HEIGHTS = {**{v: k for k, v in enumerate(ascii_lowercase)}, "S": 0, "E": 25}


class Mark(Flag):
    S = auto()
    E = auto()


@dataclass
class Square:
    x: int
    y: int
    elevation: str = ""
    mark: Mark | None = None

    @property
    def height(self):
        return HEIGHTS.get(self.elevation, 0)

    def __add__(self, other):
        return Square(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Square(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return self.elevation


class Direction(Enum):
    R = Square(1, 0)
    L = Square(-1, 0)
    U = Square(0, -1)
    D = Square(0, 1)
