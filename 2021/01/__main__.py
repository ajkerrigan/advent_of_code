from itertools import pairwise
from pathlib import Path

from more_itertools import sliding_window
from pkg_resources import resource_filename

data = [
    int(x) for x in Path(resource_filename(__name__, "input")).read_text().splitlines()
]

# pairwise is new in python 3.10, let's play
part_1 = sum(j > i for i, j in pairwise(data))
print(f"Part 1: {part_1}")

# ehhhh pairwise needs some help here - let's go lazy mode and import
# more junk
#
# just heard about more-itertools today, another new toy?
part_2 = sum(sum(j) > sum(i) for i, j in pairwise(sliding_window(data, 3)))
print(f"Part 2: {part_2}")
