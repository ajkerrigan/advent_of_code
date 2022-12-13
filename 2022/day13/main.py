import logging
import os
import sys
from itertools import pairwise, zip_longest
from operator import mul

logging.basicConfig(
    level=os.environ.get("AOC_VERBOSE") and logging.DEBUG or logging.WARNING
)
undefined = object()
filler = object()


def ordered(left, right):
    log = logging.getLogger(__name__)
    log.debug("comparing %r, %r", left, right)
    match left, right:
        case [int(l), int(r)]:
            if l == r:
                return undefined
            return l < r
        case [int(l), list(r)]:
            return ordered([l], r)
        case [list(l), int(r)]:
            return ordered(l, [r])
        case [list(l), list(r)]:
            for x, y in zip_longest(l, r, fillvalue=filler):
                if x is filler:
                    return True
                if y is filler:
                    return False
                log.debug("sub-comparing %r, %r", x, y)
                subcheck = ordered(x, y)
                if subcheck is not undefined:
                    return subcheck
            return undefined


def part1(data: str) -> int:
    properly_ordered_pairs = 0
    for i, pair in enumerate(data.split("\n\n"), start=1):
        left, right = (eval(packet) for packet in pair.splitlines())
        if ordered(left, right):
            properly_ordered_pairs += i
    return properly_ordered_pairs


def part2(data: str) -> int:
    dividers = [[[2]], [[6]]]
    packets = [eval(line) for line in data.splitlines() if line] + dividers
    all_in_order = False
    while not all_in_order:
        all_in_order = True
        for i, (left, right) in enumerate(pairwise(packets)):
            if not ordered(left, right):
                packets[i], packets[i + 1] = packets[i + 1], packets[i]
                all_in_order = False
    return mul(*(i for i, packet in enumerate(packets, start=1) if packet in dividers))


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
