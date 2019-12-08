from collections import Counter
from functools import partial
from itertools import zip_longest, dropwhile
from enum import IntEnum

class PixelColor(IntEnum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def get_num_count(layer, num):
    return sum(1 for digit in layer if int(digit) == num)

def get_layers(data, width, height):
    return grouper(data, width * height)

def get_rows(layer, width):
    return grouper(layer, width)

def flatten_layers(layers):
    for position in zip(*layers):
        visible = dropwhile(lambda x: int(x) == PixelColor.TRANSPARENT, position)
        yield '*' if int(next(visible)) == PixelColor.WHITE else ' '

if __name__ == '__main__':
    width, height = (25, 6)
    with open('day8_input.txt', 'r') as f:
        data = f.read().strip()
    layers = get_layers(data, width, height)
    rendered_layer = flatten_layers(layers)
    rendered_rows = (''.join(row) for row in get_rows(rendered_layer, width))
    print('\n'.join(rendered_rows))
