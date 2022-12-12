import sys
from coordinates import Square, Direction, Mark
from copy import deepcopy


def build_grid(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, square in enumerate(line):
            grid[(x, y)] = Square(x, y, square, getattr(Mark, square, None))
    return grid


def print_grid(grid):
    xmax, ymax = (val + 1 for val in max(grid))
    for y in range(ymax):
        print("".join(str(grid[x, y]) for x in range(xmax)))


def part1(data: str) -> int:
    grid = build_grid(data)
    print_grid(grid)
    start = next(point for point in grid.values() if point.mark == Mark.S)
    visited = {start}
    print(start)
    print(visited)
    paths = [[start]]
    hit_end = False
    while not hit_end:
        # print('\n'.join(''.join(str(p)) for p in paths))
        new_paths = []
        for path in sorted(paths, key=len):
            last_step = path[-1]
            next_steps = [grid.get((last_step + direction.value).coords) for direction in Direction]
            for step in next_steps:
                if not step or step.height > (last_step.height + 1):
                    continue
                if step in visited:
                    continue
                new_paths.append(deepcopy(path) + [step])
                visited.add(step)
                if step.mark == Mark.E:
                    return len(path)
        paths = new_paths



def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
