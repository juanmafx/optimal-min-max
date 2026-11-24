# Architecture

## Design goals

1. Keep the algorithm independent of input and output.
2. Use constant memory for any stream length.
3. Make each result reproducible and each claim testable.
4. Keep the runtime free of third-party dependencies.

## Module structure

```text
src/py_low_hig/
  __init__.py          public API and version
  __main__.py          python -m entry point
  core/
    bounds.py          optimal and baseline comparison counts
    extrema.py         Extrema result and StreamingExtrema tracker
  parsing/
    tokens.py          stop word and bounded integer parsing
  sampling/
    uniform.py         seeded uniform integer stream
  cli/
    session.py         interactive loop with injected input and output
    main.py            argument parsing and command dispatch
```

Dependencies point inward:

```text
cli --> parsing
cli --> sampling
cli --> core
```

`core`, `parsing`, and `sampling` do not import each other or perform I/O. This project has no client/server split, so it has no `frontend/` or `backend/` directories.

## Algorithm

A naive scan compares each new value with both the current minimum and maximum, using `2(n - 1)` comparisons. The pairwise method processes values two at a time:

1. Compare the two values with each other.
2. Compare the smaller with the current minimum.
3. Compare the larger with the current maximum.

That is three comparisons per two values. `StreamingExtrema` holds at most one unpaired value, so it does not need the input length in advance. `snapshot()` accounts for that value without changing the tracker state.

## Complexity

| Operation | Comparisons | Time | Extra memory |
| --- | --- | --- | --- |
| `add` | 0, 1, or 3 | O(1) comparisons | O(1) values |
| `snapshot` | 0 or 2 | O(1) comparisons | O(1) values |
| `find_extrema` on n values | `ceil(3n / 2) - 2` | O(n) comparisons | O(1) values |
| Naive scan on n values | `2(n - 1)` | O(n) comparisons | O(1) values |

Comparison counts are exact for every input. `ceil(3n / 2) - 2` matches Pohl's 1972 lower bound for finding both extrema by comparisons, so no comparison-based algorithm has a better worst case.

Python integers have arbitrary precision, so the cost of one comparison grows with operand size. The O(1) entries count comparisons and stored values rather than bit operations. Fewer comparisons also do not guarantee lower wall-clock time in CPython, and this project makes no speed claim.

## Verification strategy

| Layer | Evidence |
| --- | --- |
| Unit | Known sequences, boundaries, and error paths |
| Property | Agreement with `min`/`max`, exact comparison count, permutation invariance, correct prefix snapshots |
| Statistical | Chi-square goodness of fit for the minimum and maximum of three uniform draws from 1 to 6, using 12,000 trials, a fixed seed, and alpha 0.001 |
| Database | Idempotent schema creation and constraint enforcement |
| End-to-end | Exact transcript through `python -m py_low_hig` |

For a discrete uniform variable on `1..m` and sample size `k`, the expected distribution is `P(max = v) = (v^k - (v - 1)^k) / m^k`, and `P(min = v) = P(max = m + 1 - v)`.

## Reproducibility

Sampling uses a local `random.Random(seed)` instance and no global state. Hypothesis runs derandomized with no example database.

## Recommended deployment

Run it as a local command-line tool or import it as a library. It needs no service, network access, or database. If run results must be kept, write them from a separate layer into the optional schema in `db/schema.sql` with parameterized statements.
