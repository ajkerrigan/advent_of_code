import sys

data = sys.stdin.readlines()

# Second attempt inspired by the awk-fu at:
# https://github.com/0ceanlight/AoC-2021/blob/main/2-2.awk

horiz, depth = 0, 0
for line in data:
	direction, magnitude = line.split()
	magnitude = int(magnitude)
	match direction:
		case 'down':
			depth += magnitude
		case 'up':
			depth -= magnitude
		case 'forward':
			horiz += magnitude

print(horiz * depth)

aim, horiz, depth = 0, 0, 0
for line in data:
	direction, magnitude = line.split()
	magnitude = int(magnitude)
	match direction:
		case 'down':
			aim += magnitude
		case 'up':
			aim -= magnitude
		case 'forward':
			horiz += magnitude
			depth += (magnitude * aim)

print(horiz * depth)
