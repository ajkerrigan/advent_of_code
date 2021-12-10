import sys
from collections import namedtuple

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

autocomplete_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

Score = namedtuple("Score", ["completions", "errors"])


def get_line_score(line):
    chunks = []
    it = iter(line)

    # Find syntax errors
    for ch in it:
        if ch in pairs:
            chunks.append(ch)
        elif ch == pairs[chunks[-1]]:
            chunks.pop()
        elif ch in pairs.values():
            return Score(0, error_points[ch])

    # No syntax errors, so the line is incomplete
    autocomplete_score = 0
    for ch in chunks[::-1]:
        autocomplete_score = autocomplete_score * 5 + autocomplete_points[pairs[ch]]
    return Score(autocomplete_score, 0)


if __name__ == "__main__":
    data = sys.stdin.readlines()
    error_score = sum(get_line_score(line.strip()).errors for line in data)
    print(f"Part 1: {error_score}")

    autocomplete_points = [get_line_score(line).completions for line in data]
    sorted_scores = sorted(s for s in autocomplete_points if s > 0)
    print(f"Part 2: {sorted_scores[int(len(sorted_scores)/2)]}")
