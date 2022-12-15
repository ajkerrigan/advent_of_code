import logging
import os
import re
import sys
from itertools import product, islice
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


def beacon_sweep(grid, row):
    sensors = [
        point
        for point in grid.values()
        if point.mark == Mark.SENSOR
        and abs(row - point.y) <= point.taxi_distance(point.buddy)
    ]
    log = logging.getLogger("beacon_sweep")
    for sensor in sensors:
        log.debug("sensor: %s", sensor.coords)
        beacon_distance = sensor.taxi_distance(sensor.buddy)
        log.debug("beacon distance: %d", beacon_distance)
        x_coords = [
            x for x in range(sensor.x - beacon_distance, sensor.x + beacon_distance)
        ]
        log.debug("checking %d coords: %r ...", len(x_coords), x_coords[:10])
        for x_coord in x_coords:
            if sensor.taxi_distance((x_coord, row)) > beacon_distance:
                continue
            grid.setdefault((x_coord, row), Point(x_coord, row, Mark.NO_BEACON))
    return grid


def sweep_row(grid, row):
    return sum(v.mark == Mark.NO_BEACON for k, v in grid.items() if k[1] == row)


def part1(data: str) -> int:
    grid = build_grid(data)
    row = 10 if len(grid) == 20 else 2_000_000
    grid = beacon_sweep(grid, row)
    print_grid(grid)
    return sweep_row(grid, row)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
