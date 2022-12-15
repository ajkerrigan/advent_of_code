import logging
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import partial

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


def beacon_sweep_sensor(grid, row, sensor):
    log = logging.getLogger("beacon_sweep_sensor")
    log.debug("sensor: %s", sensor.coords)
    beacon_distance = sensor.taxi_distance(sensor.buddy)
    log.debug("beacon distance: %d", beacon_distance)
    x_coords = (
        x for x in range(sensor.x - beacon_distance, sensor.x + beacon_distance)
    )
    return {
        (x_coord, row)
        for x_coord in x_coords
        if sensor.taxi_distance((x_coord, row)) <= beacon_distance
        and not grid.get((x_coord, row))
    }


def beacon_sweep(grid, row):
    sensors = (
        point
        for point in grid.values()
        if point.mark == Mark.SENSOR
        and abs(row - point.y) <= point.taxi_distance(point.buddy)
    )

    sweeper = partial(beacon_sweep_sensor, grid, row)
    with ProcessPoolExecutor() as executor:
        return set.union(*(executor.map(sweeper, sensors)))


def part1(data: str) -> int:
    grid = build_grid(data)
    is_sample = len(grid) == 20
    row = 10 if is_sample else 2_000_000
    if is_sample:
        print_grid(grid)
    no_beacons = beacon_sweep(grid, row)
    return len(no_beacons)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
