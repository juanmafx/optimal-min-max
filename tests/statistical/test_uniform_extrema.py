from collections import Counter

import pytest

from py_low_hig.core.extrema import find_extrema
from py_low_hig.sampling.uniform import uniform_integers

FACES = 6
SAMPLE_SIZE = 3
TRIALS = 12_000
CHI_SQUARE_CRITICAL_DF5_ALPHA_0001 = 20.515


def _maximum_probability(value: int) -> float:
    return float((value**SAMPLE_SIZE - (value - 1) ** SAMPLE_SIZE) / FACES**SAMPLE_SIZE)


def _minimum_probability(value: int) -> float:
    return _maximum_probability(FACES + 1 - value)


@pytest.mark.parametrize(
    ("attribute", "probability"),
    [("maximum", _maximum_probability), ("minimum", _minimum_probability)],
)
def test_extrema_follow_order_statistic_distribution(attribute: str, probability: object) -> None:
    assert callable(probability)
    stream = uniform_integers(TRIALS * SAMPLE_SIZE, 1, FACES, seed=2026)
    observed: Counter[int] = Counter()
    for _ in range(TRIALS):
        result = find_extrema(next(stream) for _ in range(SAMPLE_SIZE))
        assert result is not None
        observed[getattr(result, attribute)] += 1
    statistic = sum(
        (observed[value] - TRIALS * probability(value)) ** 2 / (TRIALS * probability(value))
        for value in range(1, FACES + 1)
    )
    assert statistic < CHI_SQUARE_CRITICAL_DF5_ALPHA_0001
