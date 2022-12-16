import logging
import os
import re
import sys
from itertools import product

from coordinates import Mark, Point

logging.basicConfig(
    level=logging.DEBUG if os.environ.get("AOC_VERBOSE") else logging.WARNING
)


def build_grid(data):
    grid = {}

    for line in data.splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall(r"-?\d+", line))
        beacon = Point(beacon_x, beacon_y, Mark.BEACON)
        sensor = Point(sensor_x, sensor_y, Mark.SENSOR)
        sensor.buddy = beacon
        grid[sensor_x, sensor_y] = sensor
        grid[beacon_x, beacon_y] = beacon

    return grid


def print_grid(grid):
    log = logging.getLogger("print_grid")
    (xmin, xmax), (ymin, ymax) = ((min(pos), max(pos) + 1) for pos in zip(*grid))
    for y in range(ymin, ymax):
        log.debug(
            f"{y:-{len(str(ymax)) + 1}}"
            + "".join(str(grid.get((x, y), Mark.AIR)) for x in range(xmin, xmax))
        )


def beacon_sweep(grid, xrange, yrange):
    log = logging.getLogger("beacon_sweep")
    sensors = tuple(point for point in grid.values() if point.mark == Mark.SENSOR)
    possibilities = set(product(xrange, yrange))
    for sensor in sensors:
        log.debug("sweeping sensor %r", sensor)
        sensor_range = set(
            product(
                range(
                    max(sensor.x - sensor.buddy_distance, xrange.start),
                    min(sensor.x + sensor.buddy_distance + 1, xrange.stop),
                ),
                range(
                    max(sensor.y - sensor.buddy_distance, yrange.start),
                    min(sensor.y + sensor.buddy_distance + 1, yrange.stop),
                ),
            )
        )
        sweep_range = sensor_range & possibilities
        possibilities -= {
            coord
            for coord in sweep_range
            if sensor.taxi_distance(coord) <= sensor.buddy_distance
        }
    return possibilities


def part1(data: str) -> int:
    grid = build_grid(data)
    is_sample = len(grid) == 20
    y = 10 if is_sample else 2_000_000
    if is_sample:
        print_grid(grid)
    sensors = tuple(point for point in grid.values() if point.mark == Mark.SENSOR)
    xmin = min(s.x - s.buddy_distance for s in sensors)
    xmax = max(s.x + s.buddy_distance for s in sensors)
    possibilities = beacon_sweep(grid, range(xmin, xmax + 1), range(y, y + 1))
    return xmax - xmin - len(possibilities)


def part2(data: str) -> int:
    grid = build_grid(data)
    is_sample = len(grid) == 20
    maxval = 20 if is_sample else 4_000_000
    if is_sample:
        print_grid(grid)
    possibilities = beacon_sweep(grid, range(maxval + 1), range(maxval + 1))
    distress_beacon = possibilities.pop()
    assert not possibilities
    return distress_beacon[0] * 4_000_000 + distress_beacon[1]


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
