import pytest

from py_low_hig.sampling.uniform import uniform_integers


def test_same_seed_same_sequence() -> None:
    assert list(uniform_integers(50, 0, 99, 1)) == list(uniform_integers(50, 0, 99, 1))


def test_different_seed_different_sequence() -> None:
    assert list(uniform_integers(50, 0, 10**9, 1)) != list(uniform_integers(50, 0, 10**9, 2))


@pytest.mark.parametrize(("count", "low", "high"), [(-1, 0, 1), (1, 2, 1)])
def test_invalid_arguments_fail_eagerly(count: int, low: int, high: int) -> None:
    with pytest.raises(ValueError, match="must not"):
        uniform_integers(count, low, high, 0)


def test_negative_seed_is_rejected() -> None:
    with pytest.raises(ValueError, match="seed must not be negative"):
        uniform_integers(1, 0, 1, -5)
