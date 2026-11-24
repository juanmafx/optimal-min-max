import random

from hypothesis import given
from hypothesis import strategies as st

from py_low_hig.core.bounds import baseline_comparisons, optimal_comparisons
from py_low_hig.core.extrema import StreamingExtrema, find_extrema
from py_low_hig.parsing.tokens import parse_integer

integer_lists = st.lists(st.integers(), min_size=1, max_size=200)


@given(integer_lists)
def test_matches_builtin_min_and_max(values: list[int]) -> None:
    result = find_extrema(values)
    assert result is not None
    assert (result.minimum, result.maximum, result.count) == (min(values), max(values), len(values))


@given(integer_lists)
def test_comparison_count_equals_optimal_bound(values: list[int]) -> None:
    result = find_extrema(values)
    assert result is not None
    assert result.comparisons == optimal_comparisons(len(values))
    assert result.comparisons <= baseline_comparisons(len(values))


@given(integer_lists, st.randoms(use_true_random=False))
def test_extrema_are_permutation_invariant(values: list[int], rng: random.Random) -> None:
    shuffled = list(values)
    rng.shuffle(shuffled)
    first, second = find_extrema(values), find_extrema(shuffled)
    assert first is not None
    assert second is not None
    assert (first.minimum, first.maximum) == (second.minimum, second.maximum)


@given(integer_lists)
def test_every_prefix_snapshot_is_correct(values: list[int]) -> None:
    tracker = StreamingExtrema()
    for index, value in enumerate(values, start=1):
        tracker.add(value)
        snapshot = tracker.snapshot()
        assert snapshot is not None
        assert snapshot.minimum == min(values[:index])
        assert snapshot.maximum == max(values[:index])


@given(st.integers(min_value=-(10**300), max_value=10**300))
def test_integer_parsing_round_trip(value: int) -> None:
    assert parse_integer(str(value)) == value


@given(st.text(max_size=64))
def test_parser_never_raises(token: str) -> None:
    assert parse_integer(token) is None or isinstance(parse_integer(token), int)
