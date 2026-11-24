from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Extrema:
    minimum: int
    maximum: int
    count: int
    comparisons: int


class StreamingExtrema:
    __slots__ = ("_bounds", "_comparisons", "_count", "_pending")

    def __init__(self) -> None:
        self._bounds: tuple[int, int] | None = None
        self._pending: int | None = None
        self._count = 0
        self._comparisons = 0

    def add(self, value: int) -> None:
        self._count += 1
        if self._pending is None:
            self._pending = value
            return
        pending, self._pending = self._pending, None
        self._comparisons += 1
        smaller, larger = (pending, value) if pending <= value else (value, pending)
        if self._bounds is None:
            self._bounds = (smaller, larger)
            return
        low, high = self._bounds
        self._comparisons += 2
        self._bounds = (smaller if smaller < low else low, larger if larger > high else high)

    def snapshot(self) -> Extrema | None:
        if self._bounds is None:
            if self._pending is None:
                return None
            return Extrema(self._pending, self._pending, self._count, self._comparisons)
        low, high = self._bounds
        if self._pending is None:
            return Extrema(low, high, self._count, self._comparisons)
        return Extrema(
            self._pending if self._pending < low else low,
            self._pending if self._pending > high else high,
            self._count,
            self._comparisons + 2,
        )


def find_extrema(values: Iterable[int]) -> Extrema | None:
    tracker = StreamingExtrema()
    for value in values:
        tracker.add(value)
    return tracker.snapshot()
