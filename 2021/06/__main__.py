import sys
from collections import Counter, deque


def make_some_fish_babies(starting_counts, days):
    d = deque(starting_counts[i] for i in range(9))
    for i in range(days):
        d.rotate(-1)
        d[6] += d[8]
    return d


data = Counter(int(num.strip()) for num in sys.stdin.readline().split(","))
print(f"Part 1: {sum(make_some_fish_babies(data, 80))}")
print(f"Part 2: {sum(make_some_fish_babies(data, 256))}")
