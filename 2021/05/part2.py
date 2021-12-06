import part1


def straight_or_diagonal_lines(dx, dy):
    return dx == 0 or dy == 0 or abs(dx) == abs(dy)


def find_danger_zones(files=["-"], constraint=straight_or_diagonal_lines):
    return part1.find_danger_zones(files, constraint)


if __name__ == "__main__":
    find_danger_zones()
