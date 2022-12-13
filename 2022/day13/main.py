import logging
import os
import sys
from itertools import zip_longest

logging.basicConfig(
    level=os.environ.get("AOC_VERBOSE") and logging.DEBUG or logging.WARNING
)
undefined = object()
filler = object()


def compare(left, right):
    log = logging.getLogger(__name__)
    log.debug("comparing %r, %r", left, right)
    match left, right:
        case [int(l), int(r)]:
            if l == r:
                return undefined
            return l < r
        case [int(l), list(r)]:
            return compare([l], r)
        case [list(l), int(r)]:
            return compare(l, [r])
        case [list(l), list(r)]:
            for x, y in zip_longest(l, r, fillvalue=filler):
                if x is filler:
                    return True
                if y is filler:
                    return False
                log.debug("sub-comparing %r, %r", x, y)
                subcheck = compare(x, y)
                if subcheck is not undefined:
                    return subcheck
            return undefined


def part1(data: str) -> int:
    properly_ordered_pairs = 0
    for i, pair in enumerate(data.split("\n\n"), start=1):
        left, right = (eval(packet) for packet in pair.splitlines())
        if compare(left, right):
            properly_ordered_pairs += i
    return properly_ordered_pairs


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
