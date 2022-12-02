import sys

# Setup
data = sys.stdin.read()
elves = [sum(int(item) for item in elf.splitlines()) for elf in data.split("\n\n")]

print(f"Part 1: {max(elves)}")

# Part 2
print(f"Part 2: {sum(elf for elf in sorted(elves, reverse=True)[:3])}")
