from __future__ import annotations
from math import ceil
from itertools import chain
import sys
from dataclasses import dataclass, field
from contextlib import suppress

@dataclass
class Node:
    value: int | Snailfish
    _value: int | Snailfish | None = field(init=False, default=None)

    def is_regular(self):
        return isinstance(self.value, int)
    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
    
    @property
    def parent(self):
        return self.value.parent if isinstance(self.value, Snailfish) else None
    @parent.setter
    def parent(self, val):
        if isinstance(self, Snailfish):
            self.value.parent = val


@dataclass
class Snailfish:
    left: int | Snailfish | None = field(init=False)
    right: int | Snailfish | None = field(init=False)
    value: int | None = None
    _left: int | Snailfish | None = field(init=False)
    _right: int | Snailfish | None = field(init=False)
    node: Node | None = field(init=False)
    parent: Snailfish | None = field(init=False, repr=False)

    def is_regular(self):
        return False

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, val):
        val.parent = self
        self._left = val

    @right.setter
    def right(self, val):
        val.parent = self
        self._right = val

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def flatten(self):
        flat = []
        if self.left:
            flat.extend(self.left.flatten())
        if self.value:
            flat.append(self)
        if self.right:
            flat.extend(self.right.flatten())
        return flat

    def explode(self):
        flat = list(self.flatten())
        target = None
        index = 0
        for i, node in enumerate(flat):
            with suppress(AttributeError):
                if node.parent.parent.parent:
                    target = node.parent
                    index = i
                    break
        if target:
            if index - 1 >= 0:
                flat[index - 1].value += target.left.value
            if index + 1 < len(flat):
                flat[index + 1].value += target.right.value
            target = Node(0)
                
                    



    def split(self):
        if self.left.is_regular() and self.left.value >= 10:
            self.left = self.__class__(self.left.value // 2, ceil(self.left.value / 2))
            return True
        if self.right.is_regular() and self.right.value >= 10:
            self.right = self.__class__(self.right.value // 2, ceil(self.right.value / 2))
            return True
        split = False
        if not self.left.is_regular():
            split = self.left.value.split()
        if not split and not self.right.is_regular():
            split = self.right.value.split()
        return split
        

    def __add__(self, other):
        return self.__class__(self, other)

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
                case '[':
                    fish.append(cls())
                case num if str.isnumeric(num):
                    numbers.append(num)
                case ']':
                    if numbers:
                        fish[-1].right = int(str(''.join(numbers)))
                        numbers = []
                    else:
                        top = fish.pop()
                        fish[-1].right = top
                    if len(fish) == 1:
                        return fish.pop()
                case ',':
                    if numbers:
                        fish[-1].left = int(str(''.join(numbers)))
                        numbers = []
                    else:
                        top = fish.pop()
                        fish[-1].left = top

if __name__ == '__main__':
    for line in sys.stdin.readlines():
        print(Snailfish.parse(line.strip()))
