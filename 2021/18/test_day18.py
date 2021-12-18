from pkg_resources import resource_filename

from main import Snailfish


def test_roundtrip():
    with open(resource_filename("main", "input")) as f:
        data = [line.strip() for line in f.readlines()]
    parsed = [
        str(Snailfish.parse(line))
        for line in data
    ]
    assert data == parsed
