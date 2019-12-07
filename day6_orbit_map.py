from dataclasses import dataclass, field
from itertools import chain
from typing import Any


@dataclass
class Object:
    name: str
    orbit_map: Any = field(repr=False)
    orbits: list = field(default_factory=list, repr=False)
    orbited_by: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.orbit_map[self.name] = self

    def add_direct_orbit(self, obj):
        self.orbits.append(obj)
        obj.orbited_by.append(self)
        if self.orbit_map.center == self:
            self.orbit_map.center = obj

    @property
    def all_orbiters(self):
        return list(
            chain(self.orbited_by, *(obj.all_orbiters for obj in self.orbited_by))
        )

    @property
    def all_orbits(self):
        return list(chain(self.orbits, *(obj.all_orbits for obj in self.orbits)))

    def travel(self, dest, num_transfers = 0):
        if dest in self.orbited_by:
            print(f'In {self} we got there')
            return num_transfers
        if dest in self.all_orbiters:
            for obj in self.orbited_by:
                if dest in obj.all_orbiters:
                    print(f'Moving rimward to {obj}...')
                    return obj.travel(dest, num_transfers + 1)
        print(f'Moving hubward to {self.orbits[0]}...')
        return self.orbits[0].travel(dest, num_transfers + 1)

@dataclass
class OrbitMap(dict):
    center: Object = field(default=None)

    @property
    def total_orbit_count(self):
        return len(self.center.orbited_by)

    @property
    def all_orbits(self):
        return list(chain.from_iterable(obj.all_orbits for _, obj in self.items()))

    def travel(self, origin, dest):
        return origin.orbits[0].travel(dest)

    def __setitem__(self, key, value):
        if not self.center or value in self.center.orbits:
            self.center = value
        return super().__setitem__(key, value)


def parse_orbit_map(map_data):
    om = OrbitMap()
    for line in map_data.splitlines():
        inside, outside = line.split(")")
        inside = om.get(inside) or Object(inside, om)
        outside = om.get(outside) or Object(outside, om)
        outside.add_direct_orbit(inside)
    return om


if __name__ == "__main__":
    with open("day6_input.txt", "r") as f:
        map_data = f.read()
    om = OrbitMap()
    for line in map_data.splitlines():
        inside, outside = line.split(")")
        inside = om.get(inside) or Object(inside, om)
        outside = om.get(outside) or Object(outside, om)
        outside.add_direct_orbit(inside)
    print(len(om.all_orbits))
    print(om.travel(om['YOU'], om['SAN']))
