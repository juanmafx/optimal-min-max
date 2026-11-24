import pytest

from py_low_hig.parsing.tokens import MAX_TOKEN_LENGTH, parse_integer


@pytest.mark.parametrize(
    ("token", "expected"), [("7", 7), ("-3", -3), ("+4", 4), (" 12 ", 12), ("1_000", 1000)]
)
def test_accepts_python_integer_literals(token: str, expected: int) -> None:
    assert parse_integer(token) == expected


@pytest.mark.parametrize("token", ["", "bob", "1.5", "0x10", "1e3", "Done", "--1"])
def test_rejects_non_integers(token: str) -> None:
    assert parse_integer(token) is None


def test_rejects_oversized_tokens_before_conversion() -> None:
    assert parse_integer("1" * (MAX_TOKEN_LENGTH + 1)) is None


def test_accepts_token_at_length_limit() -> None:
    assert parse_integer("1" * MAX_TOKEN_LENGTH) == int("1" * MAX_TOKEN_LENGTH)
