import math
from bisect import insort
from dataclasses import dataclass
from decimal import Decimal
from itertools import islice

import numpy as np


@dataclass(frozen=True, order=True)
class Coordinate:
    x: int
    y: int

    def __iter__(self):
        yield from (self.x, self.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)


def parse_map(map_data):
    return [list(row) for row in map_data.splitlines()]


def get_asteroids(matrix):
    return [
        Coordinate(xi, yi)
        for yi, y in enumerate(matrix)
        for xi, x in enumerate(y)
        if x == "#"
    ]


def get_target_info(source, dest):
    if dest == source:
        return None

    dist = math.dist(source, dest)
    straight_up = source + Coordinate(0, dist)

    if dest.x == source.x:
        angle = 0.0 if dest.y > source.y else 180.0
    else:
        a = np.array([*source])
        b = np.array([*straight_up])
        c = np.array([*dest])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(cosine_angle))
        if dest.x < source.x:
            angle = 360.0 - angle

    return round(angle, 5), dist, dest


def surrounding_asteroids(asteroids, coord):
    surrounding = []
    for roid in asteroids:
        if roid == coord:
            continue
        insort(surrounding, get_target_info(coord, roid))
    return len({a[0] for a in surrounding}), coord, surrounding


def zap(targets):
    current_angle = targets[-1][0]
    while targets:
        try:
            target = min(t for t in targets if t[0] > current_angle)
        except ValueError:
            target = min(t for t in targets)
        targets.remove(target)
        current_angle = target[0]
        yield target


if __name__ == "__main__":
    with open("day10_input.txt", "r") as f:
        map_data = f.read().strip()
    asteroids = get_asteroids(parse_map(map_data))
    in_sight, station, targets = max(
        surrounding_asteroids(asteroids, coord) for coord in asteroids
    )

    target = next(islice(zap(targets), 199, 200))[2]
    print(f"Asteroid 200 is... {target}. 100x + y = {100 * target.x + target.y}")
