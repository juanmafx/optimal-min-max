# Release Notes: 1.0.0

Status: prepared, not tagged or published.

This release turns the 2019 single-file exercise into a typed, tested Python package that finds integer extrema with the optimal number of comparisons.

## Highlights

- Constant-memory streaming with exact comparison accounting.
- Reproducible seeded samples.
- Property-based and statistical tests.
- No runtime dependencies.

## Upgrade notes

Replace `python hi_low.py` with `uv run py-low-hig`. Sessions containing at least one valid integer keep the same output. A session with none now prints `No numbers were entered.`

Python 3.12 or newer is required.

## Verification

See [reports/tests/summary.md](reports/tests/summary.md) for the recorded test run.
