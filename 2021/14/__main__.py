import sys
from itertools import pairwise
from collections import Counter


def step(pair_counts, insertion_rules):
    c = Counter()
    for k, v in pair_counts.items():
        replacement = insertion_rules.get(k)
        if replacement:
            c[k[0] + replacement] += v
            c[replacement + k[1]] += v
        else:
            c[k] += v
    return c


def apply_steps(pair_counts, n=10):
    for i in range(n):
        pair_counts = step(pair_counts, insertion_rules)

    c = Counter()
    for k, v in pair_counts.most_common():
        c[k[1]] += v

    counts = c.most_common()
    return counts[0][1] - counts[-1][1]


if __name__ == "__main__":
    template = "^" + sys.stdin.readline().strip()
    pair_counts = Counter("".join(p) for p in pairwise(template))
    insertion_rules = dict(
        (
            tuple(l.split(" -> "))
            for line in sys.stdin.readlines()
            if (l := line.strip())
        )
    )
    print(f"Part 1: {apply_steps(pair_counts, 10)}")
    print(f"Part 1: {apply_steps(pair_counts, 40)}")
