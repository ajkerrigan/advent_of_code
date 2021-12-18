from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Snailfish:
    left: int | Snailfish | None = None
    right: int | Snailfish | None = None

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def has_children(self):
        return isinstance(self.left, self.__class__) or isinstance(self.right, self.__class__)

    def explode(self, level=0):
        exploded = None
        if level == 3:
            if isinstance(self.left, self.__class__) and not self.left.has_children():
                if isinstance(self.right, int):
                    self.right += self.left.right
                    exploded = (self.left.left, None)
                else:
                    exploded = (self.right.left, self.right.right)
                self.left = 0
            elif isinstance(self.right, self.__class__) and not self.right.has_children():
                if isinstance(self.left, int):
                    self.left += self.right.left
                    exploded = (None, self.right.right)
                else:
                    exploded = (self.right.left, self.right.right)
                self.right = 0
            return exploded
        vals = self.left.explode(level + 1) if isinstance(self.left, self.__class__) else self.right.explode(level + 1) if isinstance(self.right, self.__class__) else None
        left, right = vals
        if right and isinstance(self.right, int):
            self.right += right
            right = None
        if left and isinstance(self.left, int):
            self.left += left
            left = None
        return left, right

    def split(self):
        return NotImplementedError

    def reduce(self):
        self.explode()
        self.split()

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
