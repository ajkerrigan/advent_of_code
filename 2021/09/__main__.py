import sys

grid = {}

for x, row in enumerate(sys.stdin):
    for y, col in enumerate(row.strip()):
        grid[(x, y)] = int(col)

low_points = []
for k, v in grid.items():
    x, y = k
    if v < min(
        grid.get(adj, 9) for adj in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))
    ):
        low_points.append(v)

print(sum(x + 1 for x in low_points))
