import sys
from collections import Counter
from itertools import pairwise


def step(pair_counts, insertion_rules):
    c = Counter()
    for k, v in pair_counts.items():
        if replacement := insertion_rules.get(k):
            c[k[0] + replacement] += v
            c[replacement + k[1]] += v
        else:
            c[k] += v
    return c


def apply_steps(pair_counts, n):
    for _ in range(n):
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
        l.split(" -> ") for line in sys.stdin.readlines() if (l := line.strip())
    )
    print(f"Part 1: {apply_steps(pair_counts, 10)}")
    print(f"Part 1: {apply_steps(pair_counts, 40)}")
