import pytest
from pkg_resources import resource_filename

from main import Snailfish


def test_roundtrip():
    with open(resource_filename("main", "input")) as f:
        data = [line.strip() for line in f.readlines()]
    parsed = [str(Snailfish.parse(line)) for line in data]
    assert data == parsed


@pytest.mark.parametrize(
    "start, exploded",
    [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"),
    ],
)
def test_explode(start, exploded):
    fish = Snailfish.parse(start)
    fish.explode()
    assert str(fish) == str(Snailfish.parse(exploded))


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        ),
        (
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
        ),
        (
            "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
        ),
    ],
)
def test_add_reduce(left, right, expected):
    added = Snailfish.parse(left) + Snailfish.parse(right)
    added.reduce()
    assert str(added) == expected


@pytest.mark.parametrize(
    "pair, expected",
    [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
    ],
)
def test_split(pair, expected):
    fish = Snailfish.parse(pair)
    fish.split()
    assert str(fish) == expected


@pytest.mark.parametrize(
    "pair, expected",
    [("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")],
)
def test_reduce(pair, expected):
    fish = Snailfish.parse(pair)
    fish.reduce()
    assert str(fish) == expected


@pytest.mark.parametrize(
    "pair, expected", [("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)]
)
def test_magnitude(pair, expected):
    fish = Snailfish.parse(pair)
    assert fish.magnitude() == expected


@pytest.mark.parametrize(
    "pairs, expected",
    [
        (["[1,1]", "[2,2]", "[3,3]", "[4,4]"], "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
        (
            ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"],
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6, 6]"],
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        (
            [
                "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
                "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
                "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
                "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
                "[7,[5,[[3,8],[1,4]]]]",
                "[[2,[2,2]],[8,[8,1]]]",
                "[2,9]",
                "[1,[[[9,3],9],[[9,0],[0,7]]]]",
                "[[[5,[7,4]],7],1]",
                "[[[[4,2],2],6],[8,7]]",
            ],
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ],
)
def test_multiple_additions(pairs, expected):
    assert str(sum((Snailfish.parse(p) for p in pairs), start=Snailfish())) == expected
