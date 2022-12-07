import pytest
from main import parse_term_output


@pytest.mark.parametrize(
    ("term_output", "expected"),
    [
        ("$ cd /", [(["cd", "/"], [])]),
        (
            "$ ls\ndir a\n14848514 b.txt",
            [(["ls"], [["dir", "a"], ["14848514", "b.txt"]])],
        ),
    ],
)
def test_parse_term_output(term_output, expected):
    assert parse_term_output(term_output) == expected
