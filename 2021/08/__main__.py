import sys
outputs = []
for line in sys.stdin:
    print(line)
    signal, output = line.strip().split('|')
    output_lengths = outputs.extend(out for out in output.split() if len(out) in (2,3,4,7))
    print(output_lengths)
print(len(outputs))
