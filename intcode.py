import itertools
import logging
import queue
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import astuple, dataclass, field
from enum import Enum, IntEnum
from functools import partial
from operator import add, mul
from typing import Callable, Union

END = object()


class Color(IntEnum):
    BLACK = 0
    WHITE = 1

class Mode(IntEnum):
    POSITIONAL = 0
    IMMEDIATE = 1
    RELATIVE = 2

class ComputerBehavior(IntEnum):
    DEFAULT = 0
    PAINTING_ROBOT = 1

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

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int
    color: int = Color.BLACK

    def __iter__(self):
        yield from astuple(self)
    
    def __sub__(self, other):
        return Point(*(s - o for s, o in zip(self, other)))
    
    def __add__(self, other):
        return Point(*(s + o for s, o in zip(self, other)))


class Move(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, 1)
    DOWN = Point(0, -1)


class Program:
    def __init__(self, ops, *, behavior = ComputerBehavior.DEFAULT, debug = False):
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
            9: Op(self.adjust_relative_base, 1, False),
            99: Op(END, 0, False),
        }
        self.relative_base = 0
        if debug:
            logging.basicConfig(level=logging.INFO)
        self.behavior = behavior
        if behavior == ComputerBehavior.PAINTING_ROBOT:
            self.current_position = Point(0, 0)
            self.facing = deque((Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT))
            self.grid = defaultdict(Color)
            self.grid[self.current_position] = Color.BLACK

    @staticmethod
    def parse_ops(s):
        return {i: int(val) for i, val in enumerate(s.split(","))}

    @property
    def program(self):
        return self._ops

    def store(self):
        if self.behavior == ComputerBehavior.PAINTING_ROBOT:
            return self.grid.get(self.current_position, Color.BLACK)
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

    def adjust_relative_base(self, val):
        self.relative_base += val

    def exec(self, op, mode, start_pos):
        modes = [int(m) for m in str(mode)]
        def _get_input(i, val):
            nonlocal modes
            input_mode = modes and modes.pop() or Mode.POSITIONAL
            if input_mode == Mode.IMMEDIATE:
                return val
            if input_mode == Mode.POSITIONAL:
                return self.program.get(val, 0)
            if input_mode == Mode.RELATIVE:
                return self.program.get(self.relative_base + val, 0)
            raise ValueError(f"Unknown mode: {input_mode}")

        inputs = [
            _get_input(i, val)
            for i, val in enumerate(self.program[k] for k in range(start_pos + 1, start_pos + op.input_count + 1))
        ]
        logging.info(f'{op=}, {mode=}, {start_pos=}, {inputs=}')
        result = OpResult(op.func(*inputs))
        if result.value is not None:
            if op.produces_output:
                output_key = self.program[start_pos + 1 + op.input_count]
                output_mode = modes and modes.pop() or 0
                output_key += self.relative_base if output_mode == Mode.RELATIVE else 0
                logging.info(f'Storing {result} at position {output_key}')
                self.program[output_key] = result.value
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
            if jump is None:
                i = i + 1 + op.input_count + (1 if op.produces_output else 0)
            else:
                i = jump
            if self.behavior == ComputerBehavior.PAINTING_ROBOT and self.outq.qsize() == 2:
                self.grid[self.current_position] = Color(self.outq.get())
                self.facing.rotate(self.outq.get() and -1 or 1)
                self.current_position = self.current_position + self.facing[0].value
        return
