from dataclasses import dataclass
from enum import IntEnum
from operator import add, mul
from typing import Callable, Union

END = object()


class Mode(IntEnum):
    POSITIONAL = 0
    IMMEDIATE = 1


@dataclass(frozen=True)
class Op:
    func: Union[Callable, object]
    input_count: int
    produces_output: bool


@dataclass
class OpResult:
    value: Union[int, None]
    jump: Union[int, None] = None

    def __init__(self, val):
        if isinstance(val, tuple):
            self.value, self.jump = val
        else:
            self.value = val


class Program:
    def __init__(self, ops):
        self._ops = self.parse_ops(ops)
        self.opcodes = {
            1: Op(add, 2, True),
            2: Op(mul, 2, True),
            3: Op(self.store, 0, True),
            4: Op(self.output, 1, False),
            5: Op(self.jump_if_true, 2, False),
            6: Op(self.jump_if_false, 2, False),
            7: Op(self.lt, 2, True),
            8: Op(self.eq, 2, True),
            99: Op(END, 0, False),
        }

    @staticmethod
    def parse_ops(s):
        return [int(i) for i in s.split(",")]

    @property
    def program(self):
        return self._ops

    def store(self):
        return self._input

    def output(self, val):
        return val

    def jump_if_true(self, cond, ptrval):
        return None, ptrval if cond != 0 else None

    def jump_if_false(self, cond, ptrval):
        return None, ptrval if cond == 0 else None

    def lt(self, first, second):
        return 1 if first < second else 0

    def eq(self, first, second):
        return 1 if first == second else 0

    def exec(self, op, mode, start_pos):
        def _get_input(i, val, mode):
            if (input_mode := (mode // 10 ** i % 10)) == Mode.IMMEDIATE:
                return val
            if input_mode == Mode.POSITIONAL:
                return self.program[val]
            raise ValueError(f"Unknown mode: {input_mode}")

        inputs = [
            _get_input(i, val, mode)
            for i, val in enumerate(
                self.program[start_pos + 1 : start_pos + 1 + op.input_count]
            )
        ]
        result = OpResult(op.func(*inputs))
        if op.produces_output:
            self.program[self.program[start_pos + 1 + op.input_count]] = result.value
        else:
            print(result.value)
        return result.jump

    def run(self, input_):
        self._input = input_
        i = 0
        while True:
            mode, opcode = divmod(self.program[i], 100)
            op = self.opcodes[opcode]
            if op.func == END:
                break
            jump = self.exec(op, mode, i)
            i = jump or i + 1 + op.input_count + (1 if op.produces_output else 0)


if __name__ == "__main__":
    pgm = Program(
        """
    3,225,1,225,6,6,1100,1,238,225,104,0,1101,69,55,225,1001,144,76,224,101,-139,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,60,49,225,1102,51,78,225,1101,82,33,224,1001,224,-115,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,1102,69,5,225,2,39,13,224,1001,224,-4140,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,101,42,44,224,101,-120,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,68,49,224,101,-3332,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,50,27,225,1102,5,63,225,1002,139,75,224,1001,224,-3750,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,102,79,213,224,1001,224,-2844,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1,217,69,224,1001,224,-95,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,36,37,225,1101,26,16,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,102,2,223,223,1006,224,329,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,434,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,449,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,479,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,107,677,677,224,1002,223,2,223,1006,224,509,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,584,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,599,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,644,1001,223,1,223,108,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226
    """
    )

    pgm.run(5)
