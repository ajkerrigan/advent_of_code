import logging
import sys


def find_marker(signal: str, marker_length: int) -> int:
    """Find a sequence of unique characters in a signal

    Given a character sequence, find the first occurrence
    of `marker_length` distinct characters. Return the
    position of the end of that marker.
    """
    for position, chunk in enumerate(
        # Python 3.10 brought itertools.pairwise(), replacing
        # previous patterns like this for fetching overlapping pairs
        # from a sequence:
        #
        # zip(my_list, my_list[1:])
        # (https://docs.python.org/3/library/itertools.html?highlight=itertools#itertools.pairwise)  # noqa
        #
        # This makes the offset zip approach work for subsequences of arbitrary length,
        # because zip(signal, signal[1:], signal[2:], signal[3:]) is pretty dang tedious.
        zip(*(signal[i:] for i in range(marker_length))), start=marker_length
    ):
        if len(set(chunk)) == marker_length:
            return position


def part1(data: str) -> int:
    """Find a start-of-packer marker in the signal"""
    return find_marker(data, 4)


def part2(data: str) -> int:
    """Find a start-of-message marker in the signal"""
    return find_marker(data, 14)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
