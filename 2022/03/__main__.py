import logging
import sys
from string import ascii_letters


def part1(data):
    log = logging.getLogger("part1")
    total_priority = 0
    for sack in data.splitlines():
        log.info("rucksack: %s", sack)
        mid = len(sack) // 2
        compartments = sack[:mid], sack[mid:]
        log.info("compartments: %s, %s", *compartments)
        common = set.intersection(*(set(c) for c in compartments))
        log.info("common item: %s", common)
        assert len(common) == 1, "only expected one common item across compartments"
        priority = ascii_letters.index(common.pop()) + 1
        log.info("priority: %s", priority)
        total_priority += priority
    return total_priority


def part2(data):
    total_priority = 0
    # grouping logic shamelessly stolen from the grouper recipe here
    # https://docs.python.org/3/library/itertools.html?highlight=grouper#itertools-recipes
    for group in zip(*([iter(data.splitlines())] * 3)):
        common = set.intersection(*(set(g) for g in group))
        assert len(common) == 1, "only expected one common item across elves"
        total_priority += ascii_letters.index(common.pop()) + 1
    return total_priority


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
