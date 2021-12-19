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
        ('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[15,[0,13]]],[1,1]]'),
        ('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    ]
)
def test_explode(start, exploded):
    fish = Snailfish.parse(start)
    fish.explode()
    assert str(fish) == str(Snailfish.parse(exploded))

@pytest.mark.parametrize(
    'left, right, expected',
    [
        ('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]', '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
    ]
)
def test_add(left, right, expected):
    fish = Snailfish.parse(left) + Snailfish.parse(right)
    assert str(fish) == expected

@pytest.mark.parametrize(
    'left, right, expected',
    [
        ('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    ]
)
def test_add_reduce(left, right, expected):
    added = Snailfish.parse(left) + Snailfish.parse(right)
    added.reduce()
    assert str(added) == expected

@pytest.mark.parametrize(
    'pair, expected', [
        ('[[[[0,7],4],[15,[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'),
        ('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')
    ]
)
def test_split(pair, expected):
    fish = Snailfish.parse(pair)
    fish.split()
    assert str(fish) == expected

@pytest.mark.parametrize(
    'pair, expected', [
        ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    ]
)
def test_reduce(pair, expected):
    fish = Snailfish.parse(pair)
    fish.reduce()
    assert str(fish) == expected
