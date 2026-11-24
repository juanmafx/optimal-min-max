import io
import json
import runpy

import pytest

from py_low_hig import __version__
from py_low_hig.cli.main import INTERRUPTED_EXIT_CODE, MAX_SAMPLE_COUNT, main
from py_low_hig.cli.session import PROMPT
from py_low_hig.parsing.tokens import MAX_TOKEN_LENGTH


class _TerminalInput(io.StringIO):
    def isatty(self) -> bool:
        return True


class _InterruptedInput:
    def isatty(self) -> bool:
        return False

    def readline(self, _size: int = -1, /) -> str:
        raise KeyboardInterrupt


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as raised:
        main(["--version"])
    assert raised.value.code == 0
    assert __version__ in capsys.readouterr().out


@pytest.mark.parametrize("argv", [[], ["interactive"]])
def test_interactive_modes(
    argv: list[str], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n9\ndone\n"))
    assert main(argv) == 0
    assert capsys.readouterr().out == f"{PROMPT * 3}Maximum is 9\nMinimum is 4\n"


def test_terminal_input_uses_builtin_input(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    tokens = iter(["4", "9", "done"])
    monkeypatch.setattr("sys.stdin", _TerminalInput())
    monkeypatch.setattr("builtins.input", lambda _prompt: next(tokens))
    assert main([]) == 0
    assert capsys.readouterr().out == "Maximum is 9\nMinimum is 4\n"


def test_undecodable_stdin_is_reported_as_invalid(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    raw = io.BytesIO(b"5\n\xff\n9\ndone\n")
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(raw, encoding="utf-8"))
    assert main([]) == 0
    assert capsys.readouterr().out == (
        f"{PROMPT * 2}Invalid input\n{PROMPT * 2}Maximum is 9\nMinimum is 5\n"
    )


def test_keyboard_interrupt_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.stdin", _InterruptedInput())
    assert main([]) == INTERRUPTED_EXIT_CODE


def test_sample_json_is_reproducible(capsys: pytest.CaptureFixture[str]) -> None:
    argv = ["sample", "--count", "1001", "--low", "-50", "--high", "50", "--seed", "7", "--json"]
    assert main(argv) == 0
    first = capsys.readouterr().out
    assert main(argv) == 0
    assert capsys.readouterr().out == first
    report = json.loads(first)
    assert report["count"] == 1001
    assert report["comparisons"] == 1500
    assert report["baseline_comparisons"] == 2000
    assert -50 <= report["minimum"] <= report["maximum"] <= 50


def test_sample_text_output(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["sample", "--count", "2", "--low", "3", "--high", "3"]) == 0
    output = capsys.readouterr().out
    assert "minimum: 3" in output
    assert "maximum: 3" in output


@pytest.mark.parametrize(
    "argv",
    [
        ["sample", "--count", "0"],
        ["sample", "--count", str(MAX_SAMPLE_COUNT + 1)],
        ["sample", "--count", "abc"],
        ["sample", "--count", "1", "--low", "2", "--high", "1"],
        ["sample", "--count", "1", "--low", "9" * (MAX_TOKEN_LENGTH + 1)],
        ["sample", "--count", "1", "--high", "9" * (MAX_TOKEN_LENGTH + 1)],
        ["sample", "--count", "1", "--seed", "9" * (MAX_TOKEN_LENGTH + 1)],
        ["sample", "--count", "1", "--seed", "-5"],
    ],
)
def test_sample_rejects_invalid_arguments(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as raised:
        main(argv)
    assert raised.value.code == 2


def test_sample_guards_against_empty_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("py_low_hig.cli.main.uniform_integers", lambda *_args: iter(()))
    with pytest.raises(RuntimeError, match="no values"):
        main(["sample", "--count", "1"])


def test_module_entrypoint_exits_with_main_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["py_low_hig", "--version"])
    with pytest.raises(SystemExit) as raised:
        runpy.run_module("py_low_hig", run_name="__main__")
    assert raised.value.code == 0
