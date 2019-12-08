import itertools
import queue
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from dataclasses import dataclass, field
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
        # print(self.inputs)
        return self.inq.get()

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
        # print((op, mode, start_pos, *inputs))
        result = OpResult(op.func(*inputs))
        if result.value is not None:
            if op.produces_output:
                # print(f'Storing {result} at position {start_pos + 1 + op.input_count}')
                self.program[self.program[start_pos + 1 + op.input_count]] = result.value
            else:
                self.outq.put(result.value)
        return result.jump

    def run(self, inq, outq):
        self.inq = inq
        self.outq = outq
        i = 0
        while True:
            mode, opcode = divmod(self.program[i], 100)
            op = self.opcodes[opcode]
            if op.func == END:
                break
            jump = self.exec(op, mode, i)
            i = jump or i + 1 + op.input_count + (1 if op.produces_output else 0)
        return

def get_program():
    return Program(
                """
3,8,1001,8,10,8,105,1,0,0,21,42,67,84,109,122,203,284,365,446,99999,3,9,1002,9,3,9,1001,9,5,9,102,4,9,9,1001,9,3,9,4,9,99,3,9,1001,9,5,9,1002,9,3,9,1001,9,4,9,102,3,9,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,3,9,101,5,9,9,4,9,99,3,9,102,5,9,9,101,5,9,9,102,3,9,9,101,3,9,9,102,2,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99

                """
            )

if __name__ == "__main__":
    best_score = (-1, (-1))
    low_phase_setting = 5
    amp_count = 5
    for perm in itertools.permutations(range(low_phase_setting,low_phase_setting + amp_count)):
        qs = []
        for i, p in enumerate(perm):
            q = queue.Queue()
            q.put(p)
            if i == 0:
                q.put(0)
            qs.append(q)
        with ThreadPoolExecutor(max_workers = amp_count) as executor:
            for inq, outq in zip(qs, qs[1:] + [qs[0]]):
                executor.submit(get_program().run, inq, outq)
        score = (qs[0].queue.pop(), perm)
        if score > best_score:
            best_score = score
    print(best_score)
