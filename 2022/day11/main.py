import sys
from collections import deque
from operator import mul


def parse_monkeys(monkey_data):
    monkeys = []
    for chunk in monkey_data:
        monkey = {}
        for line in chunk.splitlines():
            prop = [s.strip() for s in line.split(":")]
            match prop:
                case ["Starting items", items]:
                    monkey["items"] = deque([int(item) for item in items.split(", ")])
                case ["Operation", op]:
                    monkey["op"] = op.partition("=")[-1]
                case ["Test", test] if "divisible by" in test:
                    monkey["test_divisor"] = int(test.split()[-1])
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
                item = monkey["items"].popleft()
                monkey.setdefault("inspect_count", 0)
                monkey["inspect_count"] += 1
                item = eval(monkey["op"], {"old": item})
                item = item // 3
                if item % monkey["test_divisor"] == 0:
                    monkeys[monkey["passtest_target"]]["items"].append(item)
                else:
                    monkeys[monkey["failtest_target"]]["items"].append(item)
    return mul(*(sorted((m["inspect_count"] for m in monkeys), reverse=True)[:2]))


def part2(data: str) -> int:
    monkeys = parse_monkeys(data.split("\n\n"))
    divisor_product = 1
    for m in monkeys:
        divisor_product *= m["test_divisor"]
    for round in range(10000):
        print(round)
        for monkey in enumerate(monkeys):
            while monkey["items"]:
                item = monkey["items"].popleft()
                monkey.setdefault("inspect_count", 0)
                monkey["inspect_count"] += 1
                item = eval(monkey["op"], {"old": item})
                item %= divisor_product
                if item % (monkey["test_divisor"]) == 0:
                    monkeys[monkey["passtest_target"]]["items"].append(item)
                else:
                    monkeys[monkey["failtest_target"]]["items"].append(item)
    return mul(*(sorted((m["inspect_count"] for m in monkeys), reverse=True)[:2]))


if __name__ == "__main__":
    data = sys.stdin.read()
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
