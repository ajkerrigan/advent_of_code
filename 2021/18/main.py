from __future__ import annotations
from math import ceil
import sys
from dataclasses import dataclass, field


@dataclass
class Snailfish:
    left: int | Snailfish | None = None
    right: int | Snailfish | None = None
    _left: int | Snailfish | None = field(init=False)
    _right: int | Snailfish | None = field(init=False)
    parent: Snailfish | None = field(init=False)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, val):
        if isinstance(val, self.__class__):
            val.parent = self
        self._left = val

    @right.setter
    def right(self, val):
        if isinstance(val, self.__class__):
            val.parent = self
        self._right = val


    def __str__(self):
        return f'[{self.left},{self.right}]'

    def has_children(self):
        return isinstance(self.left, self.__class__) or isinstance(self.right, self.__class__)

    def add_exploded_value(self, value, side):
        if side == 'right':
            if isinstance(self.left, int):
                self.left += value
                return True
            elif self.parent.add_exploded_value(value, side):
                return True
            if isinstance(self.right, int):
                self.right += value
                return True
            return self.right.add_exploded_value(value, side)    
        if isinstance(self.right, int):
            self.right += value
            return True
        elif self.right.add_exploded_value(value, side):
            return True
        if isinstance(self.left, int):
            self.left += value
            return True
        return self.left.add_exploded_value(value, side)    

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
        vals = (isinstance(self.left, self.__class__) and self.left.explode(level + 1)) or (isinstance(self.right, self.__class__) and self.right.explode(level + 1))
        if not vals:
            return
        left, right = vals
        if right:
            if isinstance(self.right, int):
                self.right += right
            elif isinstance(self.left, self.__class__):
                self.parent.add_exploded_value(right, 'right')
            right = None
        if left:
            if isinstance(self.left, int):
                self.left += left
            else:
                self.parent.add_exploded_value(left, 'left')
            left = None
        return left, right

    def split(self):
        if isinstance(self.left, int) and self.left >= 10:
            self.left = self.__class__(self.left // 2, ceil(self.left / 2))
            return True
        if isinstance(self.right, int) and self.right >= 10:
            self.right = self.__class__(self.right // 2, ceil(self.right / 2))
            return True
        split = False
        if isinstance(self.left, self.__class__):
            split = self.left.split()
        if not split and isinstance(self.right, self.__class__):
            split = self.right.split()
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
