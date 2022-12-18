import logging
import os
import re
import sys
from operator import itemgetter

from coordinates import Mark, Point
from shapely import LineString, Polygon, get_coordinates, union_all

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


def get_sensor_coverage(grid):
    """Merge all sensor diamonds into a single giant unholy polygon.
    """
    sensors = [point for point in grid.values() if point.mark == Mark.SENSOR]
    return union_all(
        [
            Polygon(
                [
                    (sensor.x - sensor.buddy_distance, sensor.y),
                    (sensor.x, sensor.y + sensor.buddy_distance),
                    (sensor.x + sensor.buddy_distance, sensor.y),
                    (sensor.x, sensor.y - sensor.buddy_distance),
                ]
            )
            for sensor in sensors
        ],
        grid_size=1.0,
    )


def part1(data: str) -> int:
    grid = build_grid(data)
    is_sample = len(grid) == 20
    y = 10 if is_sample else 2_000_000

    if is_sample:
        print_grid(grid)

    sensor_coverage = get_sensor_coverage(grid)

    # Create a line on the target y row, which covers the full x
    # range of sensors.
    xmin = min(get_coordinates(sensor_coverage), key=itemgetter(0))[0]
    xmax = max(get_coordinates(sensor_coverage), key=itemgetter(0))[0]
    search_space = LineString([(xmin, y), (xmax, y)])

    # How many points on the line are covered by sensors?
    no_beacons = search_space & sensor_coverage
    return int(no_beacons.length)


def part2(data: str) -> int:
    grid = build_grid(data)
    is_sample = len(grid) == 20
    maxval = 20 if is_sample else 4_000_000

    if is_sample:
        print_grid(grid)

    # I'm not actually sure this is the right/best way to do this,
    # but it worked for sample and real input data...
    #
    # Take the rectangle of possible beacon locations, cut out
    # any points that are covered by beacons, and find a representative
    # point in whatever's left.
    search_space = Polygon([(0, 0), (0, maxval), (maxval, maxval), (maxval, 0)])
    sensor_coverage = get_sensor_coverage(grid)
    possible_beacons = search_space - sensor_coverage
    distress_beacon = possible_beacons.representative_point()

    return int(distress_beacon.x) * 4_000_000 + int(distress_beacon.y)


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
