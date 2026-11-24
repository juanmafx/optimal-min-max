import pytest

from py_low_hig.core.bounds import baseline_comparisons, optimal_comparisons
from py_low_hig.core.extrema import Extrema, StreamingExtrema, find_extrema


def test_empty_input_has_no_extrema() -> None:
    assert find_extrema([]) is None


def test_single_value_uses_no_comparisons() -> None:
    assert find_extrema([5]) == Extrema(5, 5, 1, 0)


def test_zero_is_a_valid_pending_value() -> None:
    assert find_extrema([0, 0, 0]) == Extrema(0, 0, 3, 3)


@pytest.mark.parametrize(
    ("values", "minimum", "maximum"),
    [([7, 2, 10, 4], 2, 10), ([-1, -9, -3], -9, -1), ([3, 1, 2], 1, 3), ([1, 5, 0, 9, -2], -2, 9)],
)
def test_known_sequences(values: list[int], minimum: int, maximum: int) -> None:
    result = find_extrema(values)
    assert result is not None
    assert (result.minimum, result.maximum) == (minimum, maximum)


def test_snapshot_does_not_mutate_state() -> None:
    tracker = StreamingExtrema()
    for value in (4, 8, 1):
        tracker.add(value)
    assert tracker.snapshot() == tracker.snapshot()
    tracker.add(20)
    assert tracker.snapshot() == Extrema(1, 20, 4, 4)


@pytest.mark.parametrize("bound", [optimal_comparisons, baseline_comparisons])
def test_bounds_reject_non_positive_counts(bound: object) -> None:
    assert callable(bound)
    with pytest.raises(ValueError, match="at least 1"):
        bound(0)


@pytest.mark.parametrize(
    ("count", "expected"), [(1, 0), (2, 1), (3, 3), (4, 4), (5, 6), (100, 148)]
)
def test_optimal_bound_values(count: int, expected: int) -> None:
    assert optimal_comparisons(count) == expected
