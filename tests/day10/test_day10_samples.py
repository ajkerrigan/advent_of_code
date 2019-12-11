import pytest

from day10_monitoring_station import (
    Coordinate,
    surrounding_asteroids,
    get_asteroids,
    parse_map,
)

SAMPLE1 = """.#..#
.....
#####
....#
...##"""

SAMPLE2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

SAMPLE3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

SAMPLE4 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

SAMPLE5 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""


@pytest.mark.parametrize(
    "data, expected_visible, prime_location",
    [
        (SAMPLE1, 8, Coordinate(3, 4)),
        (SAMPLE2, 33, Coordinate(5, 8)),
        (SAMPLE3, 35, Coordinate(1, 2)),
        (SAMPLE4, 41, Coordinate(6, 3)),
        (SAMPLE5, 210, Coordinate(11, 13)),
    ],
)
def test_sample1(data, expected_visible, prime_location):
    asteroids = get_asteroids(parse_map(data))
    in_sight, station_info, *_ = max(surrounding_asteroids(asteroids, coord) for coord in asteroids)
    assert in_sight == expected_visible
    assert station_info == prime_location
