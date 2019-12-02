from itertools import product
from operator import add, mul

end = object()
OPCODES = {1: (add, 4), 2: (mul, 4), 99: (end, 0)}


def instruction(op, pgm, start_pos, num_values):
    pgm = pgm.copy()
    *inputs, output = pgm[start_pos + 1 : start_pos + num_values]
    pgm[output] = op(*(pgm[i] for i in inputs))
    return pgm


def run_program(pgm):
    pgm = pgm.copy()
    i = 0
    while True:
        op, num_values = OPCODES[pgm[i]]
        if op is end:
            break
        pgm = instruction(op, pgm, i, num_values)
        i += num_values
    return pgm


def parse_ops(s):
    return [int(i) for i in s.split(",")]


def try_solution(pgm, noun, verb):
    pgm = pgm.copy()
    pgm[1] = noun
    pgm[2] = verb
    return run_program(pgm)[0]


def find_solution(pgm, target):
    for noun, verb in product(range(100), range(100)):
        try:
            result = try_solution(pgm, noun, verb)
            if result == target:
                return (noun, verb)
        except IndexError:
            print(f"error trying {noun=}, {verb=}")


ops = parse_ops(
    "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,6,19,23,2,6,23,27,1,5,27,31,2,31,9,35,1,35,5,39,1,39,5,43,1,43,10,47,2,6,47,51,1,51,5,55,2,55,6,59,1,5,59,63,2,63,6,67,1,5,67,71,1,71,6,75,2,75,10,79,1,79,5,83,2,83,6,87,1,87,5,91,2,9,91,95,1,95,6,99,2,9,99,103,2,9,103,107,1,5,107,111,1,111,5,115,1,115,13,119,1,13,119,123,2,6,123,127,1,5,127,131,1,9,131,135,1,135,9,139,2,139,6,143,1,143,5,147,2,147,6,151,1,5,151,155,2,6,155,159,1,159,2,163,1,9,163,0,99,2,0,14,0"
)

print(find_solution(ops, 19690720))
