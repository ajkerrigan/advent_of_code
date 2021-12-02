from collections import Counter
from enum import IntEnum
from functools import partial
from itertools import dropwhile, zip_longest


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
        yield "*" if int(next(visible)) == PixelColor.WHITE else " "


def day1(layers):
    layer = min(layers, key=partial(get_num_count, num=0))
    return get_num_count(layer, 1) * get_num_count(layer, 2)


def day2(layers):
    rendered_layer = flatten_layers(layers)
    rendered_rows = ("".join(row) for row in get_rows(rendered_layer, width))
    return "\n".join(rendered_rows)


if __name__ == "__main__":
    width, height = (25, 6)
    with open("day8_input.txt", "r") as f:
        data = f.read().strip()
    layers = list(get_layers(data, width, height))
    print(day1(layers))
    print(day2(layers))
