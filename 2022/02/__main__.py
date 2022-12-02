import logging
import sys

letters = list("ABCXYZ")

logging.basicConfig(level=logging.WARN)
log = logging.getLogger("rps")
data = sys.stdin.read()
points = 0

for row in data.splitlines():
    player1, player2 = (letters.index(shape) % 3 for shape in row.split())
    log.info("starting points: %d, shapes: %s, %d, %d", points, row, player1, player2)
    points += player2 + 1
    log.info("points after shape: %d", points)
    if player1 == player2:
        points += 3
    elif (player1 + 1) % 3 == player2:
        points += 6
    log.info("points at end: %d", points)

print(f"Part 1: {points}")
