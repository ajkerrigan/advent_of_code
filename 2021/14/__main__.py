import sys
from itertools import pairwise
from collections import Counter

def step(template, insertion_rules):
    for a, b in pairwise(template):
        yield a
        if (inserted := insertion_rules.get(f'{a}{b}')):
            yield inserted
    yield template[-1]


if __name__ == '__main__':
    template = sys.stdin.readline().strip()
    insertion_rules = dict((
        tuple(l.split(' -> '))
        for line in sys.stdin.readlines()
        if (l := line.strip())
    ))
    for i in range(10):
        template = ''.join(step(template, insertion_rules))
        counts = Counter(template).most_common()
        print(counts[0][1] - counts[-1][1])
