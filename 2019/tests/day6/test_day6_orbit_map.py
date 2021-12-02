import pytest
from day6_orbit_map import parse_orbit_map

MAP_DATA = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''

def test_example_map_orbit_count():
    orbit_map = parse_orbit_map(MAP_DATA)
    assert len(list(orbit_map.all_orbits)) == 42
