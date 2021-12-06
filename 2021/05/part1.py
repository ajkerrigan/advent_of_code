import fileinput
from collections import Counter


def straight_lines(dx, dy):
    return dx == 0 or dy == 0


def find_danger_zones(files=["-"], constraint=straight_lines):
    c = Counter()
    for line in fileinput.input(files=files, encoding="utf-8"):
        x1, y1, x2, y2 = (
            int(n) for pos in line.split("->") for n in pos.strip().split(",")
        )
        dx, xmult = x2 - x1, 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy, ymult = y2 - y1, 1 if y2 > y1 else -1 if y2 < y1 else 0
        if constraint(dx, dy):
            for i in range(0, abs(dx or dy) + 1):
                c[(x1 + (i * xmult), y1 + (i * ymult))] += 1
    answer = len([k for k, v in c.items() if v > 1])
    print(f"Answer: {answer}")
    return answer


if __name__ == "__main__":
    find_danger_zones()
