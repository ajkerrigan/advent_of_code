from __future__ import annotations

import sys
from contextlib import suppress
from dataclasses import dataclass, field
from math import ceil


@dataclass
class Node:
    value: int | Snailfish
    parent: Snailfish | None = field(
        init=False, repr=False, default=None, compare=False
    )

    def __str__(self):
        return str(self.value)


@dataclass
class Snailfish:
    _left: Node | Snailfish | None = field(repr=False, default=None)
    _right: Node | Snailfish | None = field(repr=False, default=None)
    parent: Snailfish | None = field(
        init=False, repr=False, default=None, compare=False
    )

    def __post_init__(self):
        self.__class__.left = property(self.__class__.get_left, self.__class__.set_left)
        self.__class__.right = property(
            self.__class__.get_right, self.__class__.set_right
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left},{self.right})"

    def is_regular(self):
        return False

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def set_left(self, val):
        if isinstance(val, int):
            val = Node(val)
        if isinstance(val, (Node, Snailfish)):
            val.parent = self
        self._left = val

    def set_right(self, val):
        if isinstance(val, int):
            val = Node(val)
        if isinstance(val, (Node, Snailfish)):
            val.parent = self
        self._right = val

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def flatten(self):
        flat = []
        flat.extend(
            self.left.flatten() if isinstance(self.left, Snailfish) else [self.left]
        )
        flat.extend(
            self.right.flatten() if isinstance(self.right, Snailfish) else [self.right]
        )
        return flat

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

    def explode(self):
        flat = list(self.flatten())
        target = None
        index = 0
        for i, node in enumerate(flat):
            with suppress(AttributeError):
                if node.parent.parent.parent.parent.parent:
                    target = node.parent
                    index = i
                    break
        if target:
            if index - 1 >= 0:
                flat[index - 1].value += target.left.value
            if index + 2 < len(flat):
                flat[index + 2].value += target.right.value
            if target.parent.left is target:
                target.parent.left = Node(0)
            if target.parent.right is target:
                target.parent.right = Node(0)

    def split(self):
        if isinstance(self.left, Node) and self.left.value >= 10:
            val = self.left.value
            self.left = self.__class__()
            self.left.left = Node(val // 2)
            self.left.right = Node(ceil(val / 2))
            return True
        if isinstance(self.left, Snailfish):
            if self.left.split():
                return True
        if isinstance(self.right, Node) and self.right.value >= 10:
            val = self.right.value
            self.right = self.__class__()
            self.right.left = Node(val // 2)
            self.right.right = Node(ceil(val / 2))
            return True
        if isinstance(self.right, Snailfish):
            if self.right.split():
                return True

    def __add__(self, other):
        if self.left or self.right:
            newfish = self.__class__()
            newfish.left = Snailfish.parse(str(self))
            newfish.right = Snailfish.parse(str(other))
            newfish.reduce()
            return newfish
        return other

    def reduce(self):
        while True:
            start = str(self)
            self.explode()
            if str(self) != start:
                continue
            self.split()
            if str(self) == start:
                break

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
    fish = None
    # for line in sys.stdin.readlines():
    #     newfish = Snailfish.parse(line.strip())
    #     print(f'  {fish}')
    #     print(f'+ {newfish}')
    #     fish = newfish if fish is None else (fish + newfish)
    #     print(f'= {fish}')
    fish = sum(
        (Snailfish.parse(line.strip()) for line in sys.stdin.readlines()),
        start=Snailfish(),
    )
    print(f"Final sum: {fish}")
    print(fish.magnitude())
