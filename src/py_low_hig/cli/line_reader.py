from collections.abc import Callable
from typing import Protocol

from py_low_hig.parsing.tokens import MAX_TOKEN_LENGTH

DRAIN_CHUNK_SIZE = 65_536


class LineSource(Protocol):
    def readline(self, size: int = -1, /) -> str: ...


class PromptSink(Protocol):
    def write(self, text: str, /) -> int: ...

    def flush(self) -> None: ...


def bounded_line_reader(source: LineSource, sink: PromptSink) -> Callable[[str], str]:
    def read_line(prompt: str) -> str:
        sink.write(prompt)
        sink.flush()
        line = source.readline(MAX_TOKEN_LENGTH + 2)
        if not line:
            raise EOFError
        if line.endswith("\n"):
            return line[:-1]
        if len(line) > MAX_TOKEN_LENGTH:
            while (chunk := source.readline(DRAIN_CHUNK_SIZE)) and not chunk.endswith("\n"):
                pass
        return line

    return read_line
