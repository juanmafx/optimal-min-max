import random
from collections.abc import Iterator


def uniform_integers(count: int, low: int, high: int, seed: int) -> Iterator[int]:
    if count < 0:
        raise ValueError("count must not be negative")
    if low > high:
        raise ValueError("low must not exceed high")
    generator = random.Random(seed)
    return (generator.randint(low, high) for _ in range(count))
