import sys
from collections import Counter

data = sys.stdin.readlines()

ones = list(Counter(digits)['1'] for digits in zip(*(d.strip() for d in data)))
threshold = len(data) / 2
epsilon = ''.join('1' if count > threshold else '0' for count in ones)
gamma = ''.join(str(int(digit) ^ 1) for digit in epsilon)

epsilon_decimal = int(epsilon, 2)
gamma_decimal = int(gamma, 2)

print(f'Epsilon is {epsilon} (decimal: {epsilon_decimal})')
print(f'Gamma is {gamma} (decimal: {gamma_decimal})')

answer = epsilon_decimal * gamma_decimal

print(f'Part 1 answer: {answer}')
