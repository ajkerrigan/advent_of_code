import logging
import sys


def part1(data):
    marker_length = 4
    for position, chunk in enumerate(
        zip(*(data[i:] for i in range(marker_length))), start=marker_length
    ):
        if len(set(chunk)) == marker_length:
            return position


def part2(data):
    ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
