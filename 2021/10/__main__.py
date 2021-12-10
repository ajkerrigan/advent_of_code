import sys

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def get_error_score(line):
    chunks = []
    for ch in line:
        if ch in pairs:
            chunks.append(ch)
        elif ch == pairs[chunks[-1]]:
            chunks.pop()
        else:
            return scores[ch]
    return 0


if __name__ == "__main__":
    print(f"Part 1: {sum(get_error_score(line.strip()) for line in sys.stdin)}")
