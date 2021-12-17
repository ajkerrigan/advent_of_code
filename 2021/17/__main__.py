import os
import re
import sys
from itertools import product
from operator import itemgetter


def step(position, velocity):
    x1, y1 = position
    vx, vy = velocity
    return ((x1 + vx, y1 + vy), (vx and vx - int(vx / abs(vx)), vy - 1))


def visualize_grid(grid):
    ymin, ymax = (op(int(k[1]) for k in grid) for op in (min, max))
    xmin, xmax = (op(int(k[0]) for k in grid) for op in (min, max))
    return "\n".join(
        "".join(grid.get((x, y)) or "." for x in range(xmin, xmax + 1))
        for y in range(ymax, ymin - 1, -1)
    )


def fire(grid, target_bounds, velocity, visualize=False):
    pos = (0, 0)
    hit = False
    xbound, ybound = target_bounds
    v = velocity

    while pos[0] < max(xbound) + 1 and pos[1] > min(ybound) - 1:
        if grid.get((pos[0], pos[1])) == "T":
            hit = True
        grid[(pos[0], pos[1])] = "#"
        pos, v = step(pos, v)
    if visualize:
        print(visualize_grid(grid))
    return max(k[1] for k, v in grid.items() if v == "#") if hit else None


def tweak_velocity(initial, dx, dy):
    return (initial[0] + dx, initial[1] + dy)


def get_target_bounds(data):
    x1, x2, y1, y2 = [int(x) for x in re.findall(r"[-\d]+", data)]
    return ((x1, x2), (y1, y2))


def initialize_grid(target_bounds):
    xbound, ybound = target_bounds
    grid = {}
    for x, y in product(
        range(xbound[0], xbound[1] + 1), range(ybound[0], ybound[1] + 1)
    ):
        grid[(x, y)] = "T"
    grid[(0, 0)] = "S"
    return grid


def interactive_fire(grid, target_bounds):
    # Close and reopen stdin, so we can muck around with keyboard
    # input after handling a piped input file
    sys.stdin.close()
    sys.stdin = os.fdopen(1)
    velocity = (0, 0)
    max_heights = {}
    keep_going = True
    while keep_going:
        print("Top heights so far:")
        print((sorted(max_heights.items(), key=itemgetter(1), reverse=True)[:3]))
        print(f"Total hits: {len(max_heights)}")
        print(f"Current starting velocity: {velocity}")
        ch, amount = "", 1
        while not ch and amount:
            m = re.match(
                r"([hjklq])(\d*)$",
                input("Tweak (h/j/k/l)[amount] (q or ctrl-c to quit): ").strip(),
            )
            if m:
                ch, amount = m.groups()
                amount = amount and int(amount) or 1
        match ch:
            case "q":
                keep_going = False
            case "h":
                velocity = tweak_velocity(velocity, amount * -1, 0)
            case "j":
                velocity = tweak_velocity(velocity, 0, amount * -1)
            case "k":
                velocity = tweak_velocity(velocity, 0, amount * 1)
            case "l":
                velocity = tweak_velocity(velocity, amount * 1, 0)
        max_height = fire(grid.copy(), target_bounds, velocity, visualize=True)
        if max_height is not None:
            max_heights[velocity] = max_height
    return max(v for v in max_heights.values() if v), len(max_heights)


def automatic_fire(grid, target_bounds):
    max_heights = {}
    xbound, ybound = target_bounds
    vxbound = max(abs(b) for b in xbound)
    vybound = max(abs(b) for b in ybound)
    for x in range(0, vxbound + 1):
        for y in range(-vybound, vybound + 1):
            velocity = tweak_velocity((0, 0), x, y)
            max_height = fire(grid.copy(), target_bounds, velocity)
            if max_height is not None:
                max_heights[velocity] = max_height
    return max(v for v in max_heights.values() if v), len(max_heights)


if __name__ == "__main__":
    target_bounds = get_target_bounds(sys.stdin.read())
    grid = initialize_grid(target_bounds)
    start_firing = (
        interactive_fire
        if len(sys.argv) == 2 and sys.argv[1] == "--interactive"
        else automatic_fire
    )
    max_height, unique_solutions = start_firing(grid, target_bounds)
    print(f"Part 1: {max_height}")
    print(f"Part 2: {unique_solutions}")
