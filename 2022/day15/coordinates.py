from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum


class Mark(StrEnum):
    SENSOR = "S"
    BEACON = "B"
    AIR = "."


@dataclass
class Point:
    x: int
    y: int
    mark: Mark = Mark.AIR
    _buddy: Point | None = field(init=False, default=None)

    @property
    def buddy(self):
        return self._buddy

    @buddy.setter
    def buddy(self, buddy):
        self._buddy = buddy
        buddy._buddy = self

    @property
    def coords(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return self.mark


class Direction(Enum):
    R = Point(1, 0)
    L = Point(-1, 0)
    U = Point(0, -1)
    D = Point(0, 1)
