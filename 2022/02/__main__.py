import logging
import sys

logging.basicConfig(level=logging.WARN)
letters = list("ABCXYZ")


def part1(data):
    points = 0
    for row in data.splitlines():
        player1, player2 = (letters.index(shape) % 3 for shape in row.split())
        log.info(
            "starting points: %d, shapes: %s, indexes: %d, %d",
            points,
            row,
            player1,
            player2,
        )
        points += player2 + 1
        log.info("points after shape: %d", points)
        if player1 == player2:
            points += 3
        elif (player1 + 1) % 3 == player2:
            points += 6
        log.info("points at end: %d", points)
    return points


def part2(data):
    points = 0
    goal_points = [0, 3, 6]

    for row in data.splitlines():
        player1, goal = (letters.index(shape) for shape in row.split())
        log.info(
            "starting points: %d, shapes: %s, player1: %d, goal: %d",
            points,
            row,
            player1,
            goal,
        )
        points += (player1 + goal - 1) % 3 + 1
        log.info("points after shape: %d", points)
        points += goal_points[goal % 3]
        log.info("points at end: %d", points)
    return points


if __name__ == "__main__":
    log = logging.getLogger("rps")
    data = sys.stdin.read()

    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
