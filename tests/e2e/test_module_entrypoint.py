import os
import subprocess
import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src"


def _run(*args: str, stdin: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "py_low_hig", *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
        env={**os.environ, "PYTHONPATH": str(SOURCE_ROOT), "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_reference_transcript() -> None:
    completed = _run(stdin="7\n2\nbob\n10\n4\ndone\n")
    assert completed.returncode == 0
    assert completed.stdout == (
        "Enter a number: " * 3
        + "Invalid input\n"
        + "Enter a number: " * 3
        + "Maximum is 10\nMinimum is 2\n"
    )


def test_closed_stdin_exits_cleanly() -> None:
    completed = _run(stdin="")
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout.endswith("No numbers were entered.\n")
