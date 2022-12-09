from dataclasses import dataclass
from enum import Enum


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def close_gap(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        match (abs(dx), abs(dy)):
            # If the other point is touching, don't do anything
            case [adx, ady] if adx <= 1 and ady <= 1:
                return self
            # If we're chasing a point in a different row/column,
            # move diagonally
            case [adx, ady] if adx > 0 and ady > 0:
                return Point(self.x + int(dx/adx), self.y + int(dy/ady))
            # Chase one step horizontally
            case [adx, _] if adx > 1:
                return Point(self.x + int(dx/adx), self.y)
            # Chase one step vertically
            case [_, ady] if ady > 1:
                return Point(self.x, self.y + int(dy/ady))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Direction(Enum):
    R = Point(1, 0)
    L = Point(-1, 0)
    U = Point(0, -1)
    D = Point(0, 1)
