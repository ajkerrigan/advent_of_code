import logging
import sys


def part1(data):
    fully_contained_overlaps = 0
    for pair in data.splitlines():
        elf1, elf2 = [
            tuple(int(n) for n in assignment.split("-"))
            for assignment in pair.split(",")
        ]
        combined = sorted(elf1 + elf2)

        # Does one elf have both the highest and lowest
        # section numbers?
        if (combined[0], combined[-1]) in (elf1, elf2):
            fully_contained_overlaps += 1
    return fully_contained_overlaps


def part2(data):
    ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
