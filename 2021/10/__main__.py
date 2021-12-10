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

    # Find syntax errors
    for ch in line:
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
    scores = [get_line_score(line) for line in sys.stdin]
    print(f"Part 1: {sum(s.errors for s in scores)}")

    sorted_scores = sorted(s.completions for s in scores if s.completions > 0)
    print(f"Part 2: {sorted_scores[int(len(sorted_scores)/2)]}")
