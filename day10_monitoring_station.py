from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, order=True)
class Coordinate:
    x: int
    y: int

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def orientation(self, other):
        def _orientation(source, dest):
            if dest < source:
                return -1
            elif dest > source:
                return 1
            return 0

        return _orientation(self.x, other.x), _orientation(self.y, other.y)

    def slope(self, other):
        delta = self - other
        if delta.x == 0 or delta.y == 0:
            return 0
        return Decimal(delta.y / delta.x)

    def line_of_sight(self, other):
        return self.orientation(other), self.slope(other)


def parse_map(map_data):
    return [list(row) for row in map_data.splitlines()]


def get_asteroids(matrix):
    return [
        Coordinate(xi, yi)
        for yi, y in enumerate(matrix)
        for xi, x in enumerate(y)
        if x == "#"
    ]


def asteroids_in_sight(asteroids, coord):
    in_sight = 1
    return len(set(coord.line_of_sight(a) for a in asteroids if a != coord))

if __name__ == '__main__':
    with open('day10_input.txt', 'r') as f:
        map_data = f.read().strip()
    asteroids = get_asteroids(parse_map(map_data))
    best = max(((asteroids_in_sight(asteroids, coord), coord)) for coord in asteroids)
    print(best)
