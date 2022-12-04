import logging
import sys


def assignment_to_set(assignment: str) -> set:
    """Convert a section assignment range to a set of sections

    >>> assignment_to_set("2-4")
    {2, 3, 4}
    """
    low, high = tuple(int(n) for n in assignment.split("-"))
    return set(range(low, high + 1))


def parse_assignments(data: str) -> list[tuple[set]]:
    """Split cleanup assignment data into paired sets
    of assigned sections.

    assignments = '''
    2-4,6-8,
    2-5,3-7
    '''
    >>> parse_assignments(assignments)
    [
        ({2,3,4}, {6,7,8}),
        ({2,3,4,5}, {3,4,5,6,7})
    ]
    """
    return [
        tuple(assignment_to_set(assignment) for assignment in pair.split(","))
        for pair in data.splitlines()
    ]


def part1(assignments) -> int:
    """Return the number of assignments where one elf's section set
    completely overlaps the other.

    To determine complete overlap, see if the union of assignments
    matches either single elf's assignments.

    Use sum to count matches, since True == 1 and False == 0
    """
    return sum(elf1 | elf2 in (elf1, elf2) for elf1, elf2 in assignments)


def part2(assignments) -> int:
    """Return the number of elf pairs where any section assignments
    overlap.

    Sets that are disjoint don't overlap. So if sets are _not_
    disjoint, they _do_ overlap.

    Use sum to count matches, since True == 1 and False == 0
    """
    return sum(not set.isdisjoint(*assignment) for assignment in assignments)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data = sys.stdin.read()
    assignments = parse_assignments(data)
    print(f"Part 1: {part1(assignments)}")
    print(f"Part 2: {part2(assignments)}")
