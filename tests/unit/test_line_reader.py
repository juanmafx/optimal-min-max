import io

import pytest

from py_low_hig.cli.line_reader import DRAIN_CHUNK_SIZE, bounded_line_reader
from py_low_hig.parsing.tokens import MAX_TOKEN_LENGTH, parse_integer


class _RecordingInput:
    def __init__(self, text: str) -> None:
        self._source = io.StringIO(text)
        self.requests: list[int] = []

    def readline(self, size: int = -1, /) -> str:
        self.requests.append(size)
        return self._source.readline(size)


def test_writes_prompt_and_strips_newline() -> None:
    sink = io.StringIO()
    read = bounded_line_reader(io.StringIO("7\n"), sink)
    assert read("prompt: ") == "7"
    assert sink.getvalue() == "prompt: "


def test_last_line_without_newline_is_returned() -> None:
    assert bounded_line_reader(io.StringIO("7"), io.StringIO())("") == "7"


def test_blank_line_is_empty_token() -> None:
    assert bounded_line_reader(io.StringIO("\n"), io.StringIO())("") == ""


def test_end_of_input_raises() -> None:
    with pytest.raises(EOFError):
        bounded_line_reader(io.StringIO(""), io.StringIO())("")


def test_token_at_limit_is_preserved() -> None:
    token = "1" * MAX_TOKEN_LENGTH
    assert bounded_line_reader(io.StringIO(f"{token}\n"), io.StringIO())("") == token


@pytest.mark.parametrize("extra", [1, 2, 3, 200_000])
def test_oversized_line_is_invalid_and_fully_consumed(extra: int) -> None:
    source = _RecordingInput("1" * (MAX_TOKEN_LENGTH + extra) + "\n8\n")
    read = bounded_line_reader(source, io.StringIO())
    assert parse_integer(read("")) is None
    assert read("") == "8"
    assert all(0 < request <= DRAIN_CHUNK_SIZE for request in source.requests)


def test_oversized_final_line_without_newline_finishes() -> None:
    read = bounded_line_reader(io.StringIO("1" * (MAX_TOKEN_LENGTH + 5)), io.StringIO())
    assert parse_integer(read("")) is None
    with pytest.raises(EOFError):
        read("")
