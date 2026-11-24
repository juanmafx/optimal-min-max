from collections.abc import Callable, Iterable

from py_low_hig.cli.session import EMPTY_MESSAGE, INVALID_INPUT_MESSAGE, PROMPT, run_session
from py_low_hig.core.extrema import Extrema


def _reader(tokens: Iterable[str], prompts: list[str]) -> Callable[[str], str]:
    remaining = iter(tokens)

    def read(prompt: str) -> str:
        prompts.append(prompt)
        try:
            return next(remaining)
        except StopIteration as error:
            raise EOFError from error

    return read


def test_reference_session() -> None:
    prompts: list[str] = []
    output: list[str] = []
    result = run_session(_reader(["7", "2", "bob", "10", "4", "done"], prompts), output.append)
    assert result == Extrema(2, 10, 4, 4)
    assert output == [INVALID_INPUT_MESSAGE, "Maximum is 10", "Minimum is 2"]
    assert prompts == [PROMPT] * 6


def test_end_of_input_finishes_session() -> None:
    output: list[str] = []
    assert run_session(_reader(["3"], []), output.append) == Extrema(3, 3, 1, 0)
    assert output == ["Maximum is 3", "Minimum is 3"]


def test_empty_session_reports_no_numbers() -> None:
    output: list[str] = []
    assert run_session(_reader(["done"], []), output.append) is None
    assert output == [EMPTY_MESSAGE]


def test_stop_token_is_exact() -> None:
    output: list[str] = []
    run_session(_reader(["DONE", " done", "1", "done"], []), output.append)
    assert output == [INVALID_INPUT_MESSAGE, INVALID_INPUT_MESSAGE, "Maximum is 1", "Minimum is 1"]


def test_invalid_input_is_not_echoed() -> None:
    output: list[str] = []
    run_session(_reader(["\x1b[2Jpayload", "done"], []), output.append)
    assert not any("payload" in line for line in output)
