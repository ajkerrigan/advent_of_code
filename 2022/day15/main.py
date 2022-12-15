import logging
import os
import re
import sys

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
        log.debug("".join(str(grid.get((x, y), Mark.AIR)) for x in range(xmin, xmax)))


def part1(data: str) -> int:
    grid = build_grid(data)
    print_grid(grid)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
