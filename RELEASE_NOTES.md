# Release Notes: 1.0.0

Status: prepared, not tagged or released.

This release turns the 2019 single-file exercise into a typed, tested Python package that finds integer extrema with the optimal number of comparisons.

## Highlights

- Streaming that stores at most three integers, with exact comparison accounting.
- Reproducible seeded samples.
- Property-based and statistical tests.
- No runtime dependencies.

## Upgrade notes

Replace `python hi_low.py` with `uv run py-low-hig`. Sessions with at least one valid integer keep the same output, except that tokens over 4,096 characters are now invalid and undecodable bytes are reported as invalid instead of crashing. A session with no valid numbers now prints `No numbers were entered.`

Python 3.12 or newer is required.

## Verification

See [reports/tests/summary.md](reports/tests/summary.md) for the recorded test run.
