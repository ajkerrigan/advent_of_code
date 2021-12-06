from pkg_resources import resource_filename

import part1
import part2


def test_part1_sample():
    assert part1.find_danger_zones(files=[resource_filename("part1", "sample")]) == 5


def test_part2_sample():
    assert part2.find_danger_zones(files=[resource_filename("part1", "sample")]) == 12
