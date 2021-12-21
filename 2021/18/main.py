from __future__ import annotations

import sys
from dataclasses import dataclass, field
from functools import partial
from itertools import permutations
from math import ceil
from operator import attrgetter


@dataclass
class Node:
    value: int | Snailfish
    parent: Snailfish | None = field(
        init=False, repr=False, default=None, compare=False
    )

    def __str__(self):
        return str(self.value)

    def split(self):
        fish = Snailfish()
        fish.left = Node(self.value // 2)
        fish.right = Node(ceil(self.value / 2))
        return fish

    @property
    def level(self):
        return self.parent.level + 1 if self.parent else 0


@dataclass
class Snailfish:
    _left: Node | Snailfish | None = field(repr=False, default=None)
    _right: Node | Snailfish | None = field(repr=False, default=None)
    parent: Snailfish | None = field(init=False, repr=False, default=None)

    def __post_init__(self):
        self.__class__.left = property(
            partial(attrgetter("_left")),
            partial(self.__class__.set_child, attr="_left"),
        )
        self.__class__.right = property(
            partial(attrgetter("_right")),
            partial(self.__class__.set_child, attr="_right"),
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left},{self.right})"

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def __add__(self, other):
        if self.left or self.right:
            newfish = self.__class__()
            newfish.left = Snailfish.parse(str(self))
            newfish.right = Snailfish.parse(str(other))
            newfish.reduce()
            return newfish
        return other

    @property
    def level(self):
        return self.parent.level + 1 if self.parent else 0

    def get_child(self, attr):
        return getattr(self, attr)

    def set_child(self, val, attr):
        if isinstance(val, int):
            val = Node(val)
        if isinstance(val, (Node, Snailfish)):
            val.parent = self
        setattr(self, attr, val)

    def flatten(self):
        return [
            *(self.left.flatten() if isinstance(self.left, Snailfish) else [self.left]),
            *(
                self.right.flatten()
                if isinstance(self.right, Snailfish)
                else [self.right]
            ),
        ]

    def explode(self):
        flat = list(self.flatten())
        target = None
        for i, node in enumerate(flat):
            if node.level > 4:
                target = node.parent
                break
        if target:
            if i - 1 >= 0:
                flat[i - 1].value += target.left.value
            if i + 2 < len(flat):
                flat[i + 2].value += target.right.value
            if target.parent.left is target:
                target.parent.left = Node(0)
            if target.parent.right is target:
                target.parent.right = Node(0)

    def split(self):
        if isinstance(self.left, Node) and self.left.value >= 10:
            self.left = self.left.split()
            return True
        if isinstance(self.left, Snailfish) and self.left.split():
            return True
        if isinstance(self.right, Node) and self.right.value >= 10:
            self.right = self.right.split()
            return True
        if isinstance(self.right, Snailfish) and self.right.split():
            return True

    def reduce(self):
        while True:
            start = str(self)
            self.explode()
            if str(self) != start:
                continue
            self.split()
            if str(self) == start:
                break

    def magnitude(self):
        left = (
            self.left.value
            if isinstance(self.left, Node)
            else self.left.magnitude()
            if isinstance(self.left, self.__class__)
            else 0
        )
        right = (
            self.right.value
            if isinstance(self.right, Node)
            else self.right.magnitude()
            if isinstance(self.right, self.__class__)
            else 0
        )
        return 3 * left + 2 * right

    @classmethod
    def parse(cls, str_):
        fish = []
        numbers = []
        for t in str_:
            match t:
                case "[":
                    fish.append(cls())
                case num if str.isnumeric(num):
                    numbers.append(num)
                case "]":
                    if numbers:
                        fish[-1].right = int(str("".join(numbers)))
                        numbers = []
                    else:
                        top = fish.pop()
                        fish[-1].right = top
                    if len(fish) == 1:
                        return fish.pop()
                case ",":
                    if numbers:
                        fish[-1].left = int(str("".join(numbers)))
                        numbers = []
                    else:
                        top = fish.pop()
                        fish[-1].left = top


if __name__ == "__main__":
    data = [Snailfish.parse(line.strip()) for line in sys.stdin.readlines()]
    total = sum(
        data,
        start=Snailfish(),
    )
    print(f"Part 1: {total.magnitude()}")

    biggest_sum = max((a + b).magnitude() for a, b in permutations(data, 2))
    print(f"Part 2: {biggest_sum}")
