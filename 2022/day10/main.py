import sys
from dataclasses import dataclass, field
from collections import deque


@dataclass
class CPU:
    X: int = 1
    instructions: deque = field(default_factory=deque)
    instruction: str = field(init=False, repr=False, default=None)
    cycle: int = field(init=False, repr=False, default=1)

    def tick(self):
        if not self.instruction:
            self.instruction = self.instructions.popleft()
        self.instruction.duration -= 1
        if self.instruction.duration == 0:
            self.execute(self.instruction)
            self.instruction = None
        self.cycle += 1

    def execute(self, instruction):
        match instruction.type:
            case "noop":
                pass
            case "addx":
                self.X += instruction.arg


@dataclass
class Instruction:
    type: str = "noop"
    duration: int = 1
    arg: int | None = None


def part1(data: str) -> int:
    cpu = CPU()
    for line in data.splitlines():
        match line.split():
            case ["noop"]:
                cpu.instructions.append(Instruction())
            case ["addx", val]:
                cpu.instructions.append(Instruction("addx", 2, int(val)))
    signal_strengths = []
    while cpu.instructions:
        cpu.tick()
        if (cpu.cycle - 20) % 40 == 0:
            signal_strengths.append(cpu.cycle * cpu.X)
    return sum(signal_strengths)


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
