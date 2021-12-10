import sys
from collections import defaultdict


def _only_one(seq):
    """Make sure a sequence only has one value

    Yell and scream otherwise.
    """
    value = list(seq)
    assert len(value) == 1, f"{seq} has more than one value, oops"
    return value[0]


def get_line_output(line):
    """Produce a number sequence from a line of signal codes

    Each line's mapping of code letters to segment locations
    is unique, but we can derive it by examining all of a
    line's code sequences.
    """
    # Collect possible segment configurations based on
    # the number of "on" segments
    segment_count_map = defaultdict(set)

    # Map display numbers to the display segments that
    # produce them
    signal_map = {}

    # Map segments to the letters that represent them
    # Segment numbers go top to bottom, left to right
    # starting at 0
    segment_map = {}

    signals, outputs = [x.split() for x in line.strip().split("|")]

    # Find all unique segment configurations on this line
    # by the number of "on" segments in each code
    for signal in (*signals, *outputs):
        segment_count_map[len(signal)].add(tuple(sorted(signal)))

    # Map signals for the "easy" ones. So for instance,
    # number 1 is the only possible value when there are
    # 2 "on" segments.
    signal_map[1] = set(_only_one(segment_count_map[2]))
    signal_map[4] = set(_only_one(segment_count_map[4]))
    signal_map[7] = set(_only_one(segment_count_map[3]))
    signal_map[8] = set(_only_one(segment_count_map[7]))

    # Segment 2 (top right) will be on to display a 1.
    # If 6 segments are on, the bottom right will _always_ be on but the top right won't.
    segment_map[2] = signal_map[1] - set.intersection(
        *(set(x) for x in segment_count_map[6])
    )

    # Segment 3 (middle) is the only segment that is on any time 4 or 5 segments are on.
    segment_map[3] = set.intersection(
        *(set(x) for x in (segment_count_map[4] | segment_count_map[5]))
    )

    # If 6 segments are on, the result could be 0, 6 or 9.
    # Only number 6 will have segment 2 (top right) off.
    signal_map[6] = _only_one(
        y for x in segment_count_map[6] if not segment_map[2] < (y := set(x))
    )

    # 0 is the only number with 6 segments on and segment 3 (middle) off.
    signal_map[0] = _only_one(
        y
        for x in segment_count_map[6]
        if x != signal_map[6] and not segment_map[3] < (y := set(x))
    )

    # The only number left with 6 segments on is 9.
    signal_map[9] = _only_one(
        y
        for x in segment_count_map[6]
        if (y := set(x)) not in (signal_map[0], signal_map[6])
    )

    # Only number 3 can have 5 segments on, including both segments that make up a number 1.
    signal_map[3] = _only_one(
        y for x in segment_count_map[5] if len((y := set(x)) & signal_map[1]) == 2
    )

    # Number 5 has 5 segments on, but segment 2 (top right) is off.
    signal_map[5] = _only_one(
        y for x in segment_count_map[5] if not segment_map[2] <= (y := set(x))
    )

    # Number 2 is the only one left with 5 segments on.
    signal_map[2] = _only_one(
        y
        for x in segment_count_map[5]
        if (y := set(x)) not in (signal_map[3], signal_map[5])
    )

    # We'll look up display numbers by segment sequence, so invert the
    # signal map.
    signal_lookup = {tuple(sorted(v)): str(k) for k, v in signal_map.items()}

    # Mush the output numbers together.
    return int("".join(signal_lookup[tuple(sorted(output))] for output in outputs))


output_values = [get_line_output(line) for line in sys.stdin]
print(f"Answer: {sum(output_values)}")
