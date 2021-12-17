import re
import sys
from itertools import product
from operator import itemgetter


def step(position, velocity):
    x1, y1 = position
    vx, vy = velocity
    return ((x1 + vx, y1 + vy), (vx and vx - (vx / abs(vx)), vy - 1))


def visualize_grid(grid):
    ymin, ymax = (op(int(k[1]) for k in grid) for op in (min, max))
    xmin, xmax = (op(int(k[0]) for k in grid) for op in (min, max))
    return "\n".join(
        "".join(grid.get((x, y)) or "." for x in range(xmin, xmax + 1))
        for y in range(ymax, ymin - 1, -1)
    )


def fire(grid, target_bounds, velocity):
    pos = (0, 0)
    hit = False
    xbound, ybound = target_bounds

    while pos[0] < max(xbound) and pos[1] > min(ybound):
        pos, velocity = step(pos, velocity)
        if grid.get((pos[0], pos[1])) == "T":
            hit = True
        grid[(pos[0], pos[1])] = "#"
        print(pos, velocity)
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


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        target_bounds = get_target_bounds(f.read())
    grid = initialize_grid(target_bounds)
    max_heights = {}
    velocity = (5, 5)
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
        if max_height := fire(grid.copy(), target_bounds, velocity):
            max_heights[velocity] = max_height
