import logging
import os
import sys
from bisect import insort
from dataclasses import dataclass
from itertools import zip_longest
from operator import mul

logging.basicConfig(
    level=os.environ.get("AOC_VERBOSE") and logging.DEBUG or logging.WARNING
)
equals = object()
filler = object()


@dataclass
class PacketData:
    """Represent data elements in a signal packet

    Encapsulate the ordering rules of signal data,
    where elements may be lists or ints.
    """
    data: list | int

    def __post_init__(self):
        if isinstance(self.data, PacketData):
            self.data = self.data.data

    def __lt__(self, other):
        """Return whether two packet items are in the proper order

        This test may run recursively for nested items within
        packets. When tests are inconclusive, use a sentinel
        value as a signal to keep checking.
        """
        log = logging.getLogger(__name__)
        log.debug("comparing %r, %r", self, other)
        match self.data, other.data:
            case [int(l), int(r)]:
                if l == r:
                    return equals
                return l < r
            case [int(l), list(r)]:
                return PacketData([l]) < PacketData(r)
            case [list(l), int(r)]:
                return PacketData(l) < PacketData([r])
            case [list(l), list(r)]:
                for x, y in zip_longest(l, r, fillvalue=filler):
                    if x is filler:
                        return True
                    if y is filler:
                        return False
                    log.debug("sub-comparing %r, %r", x, y)
                    subcheck = PacketData(x) < PacketData(y)
                    if subcheck is not equals:
                        return subcheck
                return equals

    def __eq__(self, other):
        return self.data < other.data is equals

    def __gt__(self, other):
        return self.data < other.data is False


def part1(data: str) -> int:
    """Properly ordered pairs

    Sum the indices of all packet pairs (1-indexed) where
    those packets are properly ordered.
    """
    return sum(
        i
        for i, pair in enumerate(data.split("\n\n"), start=1)
        if [eval(p) for p in pair.splitlines()]
        == sorted((eval(p) for p in pair.splitlines()), key=PacketData)
    )


def part2(data: str) -> int:
    """Properly placed dividers

    Multiply the packet indices of two divider packets inserted
    into a sorted list.
    """
    dividers = [[[2]], [[6]]]
    packets = sorted((eval(line) for line in data.splitlines() if line), key=PacketData)
    for d in dividers:
        insort(packets, d, key=PacketData)
    return mul(*(i for i, packet in enumerate(packets, start=1) if packet in dividers))


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
