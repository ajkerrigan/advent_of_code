from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum
from functools import lru_cache


class Mark(StrEnum):
    SENSOR = "S"
    BEACON = "B"
    AIR = "."
    NO_BEACON = "#"


@dataclass
class Point:
    x: int
    y: int
    mark: Mark = Mark.AIR
    _buddy: Point | None = field(init=False, default=None)
    _buddy_distance: int = field(init=False, default=0)

    @property
    def buddy(self):
        return self._buddy

    @buddy.setter
    def buddy(self, buddy):
        self._buddy = buddy
        buddy._buddy = self
        distance = sum(abs(x - y) for x, y in zip(iter(self), iter(buddy)))
        self._buddy_distance = distance
        buddy._buddy_distance = distance

    @property
    def buddy_distance(self):
        return self._buddy_distance

    @property
    def coords(self):
        return (self.x, self.y)

    def __iter__(self):
        return iter(self.coords)

    # @lru_cache(maxsize=1000)
    def taxi_distance(self, other):
        return sum(abs(x - y) for x, y in zip(self, other))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

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
