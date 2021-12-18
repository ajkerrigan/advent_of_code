from pkg_resources import resource_filename
import pytest

from main import Snailfish


def test_roundtrip():
    with open(resource_filename("main", "input")) as f:
        data = [line.strip() for line in f.readlines()]
    parsed = [
        str(Snailfish.parse(line))
        for line in data
    ]
    assert data == parsed


@pytest.mark.parametrize(
    'start, exploded',
    [
        ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
        ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
    ]
)
def test_exploding(start, exploded):
    fish = Snailfish.parse(start)
    fish.explode()
    assert str(fish) == str(Snailfish.parse(exploded))
