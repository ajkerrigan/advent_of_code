import sys
from dataclasses import dataclass, field
from collections import deque


@dataclass
class CPU:
    X: int = 1
    instructions: deque = field(default_factory=deque)
    instruction: str = field(init=False, repr=False, default=None)
    cycle: int = field(init=False, repr=False, default=1)

    def load_instructions(self, lines):
        for line in lines.splitlines():
            match line.split():
                case ["noop"]:
                    self.instructions.append(Instruction())
                case ["addx", val]:
                    self.instructions.append(Instruction("addx", 2, int(val)))

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
class CRT:
    output_row: list = field(default_factory=list)
    output: list = field(default_factory=list)

    def draw(self, cycle, sprite):
        self.output_row.append("#" if abs((cycle % 40) - sprite - 1) <= 1 else ".")
        if cycle % 40 == 0:
            self.output.append(self.output_row)
            self.output_row = []

    @property
    def message(self):
        return "\n" + "\n".join("".join(row) for row in self.output)


@dataclass
class Instruction:
    type: str = "noop"
    duration: int = 1
    arg: int | None = None


def part1(data: str) -> int:
    cpu = CPU()
    cpu.load_instructions(data)
    signal_strengths = []
    while cpu.instructions:
        cpu.tick()
        if (cpu.cycle - 20) % 40 == 0:
            signal_strengths.append(cpu.cycle * cpu.X)
    return sum(signal_strengths)


def part2(data: str) -> str:
    cpu = CPU()
    cpu.load_instructions(data)
    crt = CRT()
    while cpu.instructions:
        crt.draw(cpu.cycle, cpu.X)
        cpu.tick()
    return crt.message


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
