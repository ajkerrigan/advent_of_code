import sys
from collections import Counter, defaultdict

data = sys.stdin.readlines()


def part1():
    ones = (Counter(digits)["1"] for digits in zip(*(d.strip() for d in data)))
    threshold = len(data) / 2
    epsilon = "".join("1" if count > threshold else "0" for count in ones)
    gamma = "".join(str(int(digit) ^ 1) for digit in epsilon)
    epsilon_decimal = int(epsilon, 2)
    gamma_decimal = int(gamma, 2)

    print(
        "[Part 1]",
        f"Epsilon: {epsilon} (decimal: {epsilon_decimal})",
        f"Gamma: {gamma} (decimal: {gamma_decimal})",
        f"Answer: {epsilon_decimal * gamma_decimal}",
        sep="\n",
    )


def find_rating(nums: list[str], keep_most_common: bool):
    for i in range(len(nums[0])):
        splits = defaultdict(list)
        for num in nums:
            splits[num[i]].append(num)
        nums = sorted(splits.values(), key=lambda val: (len(val), val[0][i]))[
            keep_most_common
        ]
        if len(nums) == 1:
            return nums[0]
    raise ValueError("Unable to find a rating")


def part2():
    nums = [num.strip() for num in data]
    oxy = find_rating(nums, True)
    co2 = find_rating(nums, False)
    oxy_decimal = int(oxy, 2)
    co2_decimal = int(co2, 2)

    print(
        "[Part 2]",
        f"Oxygen generator rating: {oxy} (decimal: {oxy_decimal})",
        f"CO2 scrubber rating: {co2} (decimal: {co2_decimal})",
        f"answer: {oxy_decimal * co2_decimal}",
        sep="\n",
    )


part1()
part2()
