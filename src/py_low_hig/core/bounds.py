def _require_positive(count: int) -> None:
    if count < 1:
        raise ValueError("count must be at least 1")


def optimal_comparisons(count: int) -> int:
    _require_positive(count)
    return (3 * count + 1) // 2 - 2


def baseline_comparisons(count: int) -> int:
    _require_positive(count)
    return 2 * (count - 1)
