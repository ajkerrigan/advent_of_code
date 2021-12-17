import sys

import re

m = re.findall(r'[-\d]+', sys.stdin.read())
print(m)
# x1, x2, y1, y2 = m.groups()
# print(x1, x2, y1, y2)
