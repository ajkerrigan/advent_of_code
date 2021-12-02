import sys
from dataclasses import dataclass
from pathlib import Path

from pkg_resources import resource_filename


@dataclass
class Sub:
    horizontal: int = 0
    depth: int = 0

    def down(self, n):
        self.depth += n

    def up(self, n):
        self.depth -= n

    def forward(self, n):
        self.horizontal += n

    def product(self):
        return self.horizontal * self.depth

    def __repr__(self):
        return f"Sub({self.horizontal, self.depth})"

    def __str__(self):
        return f"The sub is at position ({self.horizontal}, {self.depth})"


@dataclass
class SubPart2(Sub):
    aim: int = 0

    def down(self, n):
        self.aim += n

    def up(self, n):
        self.aim -= n

    def forward(self, n):
        self.horizontal += n
        self.depth += self.aim * n

    def __str__(self):
        return f"{super().__str__()} with aim: {self.aim}"


def pilot_the_thing(sub, steps):
    for line in steps:
        direction, magnitude = line.split()
        getattr(sub, direction)(int(magnitude))

    print(sub)
    print(f"Product of coordinates: {sub.product()}")


course = sys.stdin.readlines()
print("Part 1...")
pilot_the_thing(Sub(), course)

print("Part 2...")
pilot_the_thing(SubPart2(), course)
