from collections.abc import Callable

from py_low_hig.core.extrema import Extrema, StreamingExtrema
from py_low_hig.parsing.tokens import STOP_WORD, parse_integer

PROMPT = "Enter a number: "
INVALID_INPUT_MESSAGE = "Invalid input"
EMPTY_MESSAGE = "No numbers were entered."


def run_session(
    read_line: Callable[[str], str], write_line: Callable[[str], None]
) -> Extrema | None:
    tracker = StreamingExtrema()
    while True:
        try:
            token = read_line(PROMPT)
        except EOFError:
            break
        if token == STOP_WORD:
            break
        value = parse_integer(token)
        if value is None:
            write_line(INVALID_INPUT_MESSAGE)
            continue
        tracker.add(value)
    result = tracker.snapshot()
    if result is None:
        write_line(EMPTY_MESSAGE)
    else:
        write_line(f"Maximum is {result.maximum}")
        write_line(f"Minimum is {result.minimum}")
    return result
