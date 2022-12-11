import sys
from functools import partial
from operator import mul


def testfunc(number, divisor):
    return number % divisor == 0


def parse_monkeys(monkey_data):
    monkeys = []
    for chunk in monkey_data:
        monkey = {}
        for line in chunk.splitlines():
            prop = [s.strip() for s in line.split(":")]
            match prop:
                case ["Starting items", items]:
                    monkey["items"] = [int(item) for item in items.split(", ")]
                case ["Operation", op]:
                    monkey["op"] = op.partition("=")[-1]
                case ["Test", test] if "divisible by" in test:
                    monkey["test"] = partial(testfunc, divisor=int(test.split()[-1]))
                case ["If true", action]:
                    monkey["passtest_target"] = int(action.split()[-1])
                case ["If false", action]:
                    monkey["failtest_target"] = int(action.split()[-1])
        monkeys.append(monkey)
    return monkeys


def part1(data: str) -> int:
    monkeys = parse_monkeys(data.split("\n\n"))
    for _ in range(20):
        for monkey in monkeys:
            while monkey["items"]:
                item = monkey["items"].pop(0)
                monkey.setdefault("inspect_count", 0)
                monkey["inspect_count"] += 1
                item = eval(monkey["op"], {"old": item})
                item = item // 3
                if monkey["test"](item):
                    monkeys[monkey["passtest_target"]]["items"].append(item)
                else:
                    monkeys[monkey["failtest_target"]]["items"].append(item)
    return mul(*(sorted((m["inspect_count"] for m in monkeys), reverse=True)[:2]))


def part2(data: str) -> int:
    ...


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
