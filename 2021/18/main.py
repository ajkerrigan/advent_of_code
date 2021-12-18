from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Snailfish:
    left: int | Snailfish | None = None
    right: int | Snailfish | None = None

    def __str__(self):
        return f'[{self.left},{self.right}]'
    
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
