# py_low_hig

A small, fully tested Python command-line tool and library that finds the minimum and maximum of a stream of integers using the worst-case optimal number of comparisons.

> **Project history:** originally created in 2019 as a single-file exercise, modernized in 2026.

## Purpose

Given integers one at a time, report the smallest and largest seen so far, storing at most three integers and without knowing the length of the input in advance.

## Why this project exists

The original script was a learning exercise in loops, input validation, and tracking state. This version keeps the original output for sessions with at least one valid integer, apart from the input limits and error handling listed in the [changelog](CHANGELOG.md), and uses the same tiny problem to demonstrate algorithm analysis, property-based testing, reproducible experiments, and disciplined packaging. It is a study project and is not presented as production software.

## What it does

- **Interactive mode:** prompts for integers until `done` or end of input, skips invalid entries (including undecodable bytes and lines over 4,096 characters), then prints the maximum and minimum.
- **Sample mode:** generates a seeded uniform integer sample and reports its extrema, the comparisons used, and the comparisons a naive scan would use.
- **Library:** exposes `find_extrema` and the incremental `StreamingExtrema` tracker.

The runtime has no third-party dependencies.

## Architecture

```text
src/py_low_hig/
  core/       extrema algorithm and comparison bounds
  parsing/    bounded integer token parsing
  sampling/   seeded integer generation
  cli/        interactive session and argument handling
tests/        unit, property, statistical, database, end-to-end
db/           optional SQLite schema
docs/         architecture and security audit
reports/      committed output of a real test run
scripts/      test report generator
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the design and complexity analysis.

## Quick start

Requires Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run py-low-hig
```

## Usage guide

### Interactive

```console
$ printf '7\n2\nbob\n10\n4\ndone\n' | uv run python -m py_low_hig
Enter a number: Enter a number: Enter a number: Invalid input
Enter a number: Enter a number: Enter a number: Maximum is 10
Minimum is 2
```

Prompts share a line with the output here because the input is piped.

### Reproducible sample

```console
$ uv run py-low-hig sample --count 1000 --low -100 --high 100 --seed 42
seed: 42
low: -100
high: 100
count: 1000
minimum: -100
maximum: 100
comparisons: 1498
baseline_comparisons: 1998
```

Add `--json` for machine-readable output.

### Library

```python
from py_low_hig import StreamingExtrema, find_extrema

result = find_extrema([7, 2, 10, 4])
print(result.minimum, result.maximum, result.comparisons)

tracker = StreamingExtrema()
tracker.add(3)
tracker.add(9)
print(tracker.snapshot())
```

## Configuration

There are no environment variables or configuration files. `sample` accepts:

| Option | Default | Meaning |
| --- | --- | --- |
| `--count` | required | Sample size, from 1 to 10,000,000 |
| `--low` | `0` | Inclusive lower bound, at most 4,096 characters |
| `--high` | `1000000` | Inclusive upper bound, at most 4,096 characters |
| `--seed` | `0` | Non-negative pseudorandom seed, at most 4,096 characters |
| `--json` | off | Emit a JSON object |

## Database (optional)

The application does not use a database and runs without one. [db/schema.sql](db/schema.sql) is an optional SQLite schema for anyone who wants to store sample run results. It uses `STRICT` tables, which require SQLite 3.37 or newer:

```bash
sqlite3 runs.sqlite < db/schema.sql
```

## Testing

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run python scripts/generate_test_report.py
```

The suite covers unit behavior, algebraic properties with Hypothesis, a seeded chi-square check of the extrema distributions, schema constraints, and the real module entry point. The latest report is in [reports/tests/summary.md](reports/tests/summary.md).

## Security notes

The tool opens no network connections, reads no files at runtime, and stores no data. Piped input is read in bounded chunks, so an oversized line is discarded without being held in memory. Terminal input uses Python's `input`, so this memory bound applies to piped input only; the same 4,096-character check still applies before conversion. Invalid interactive input and rejected numeric options are never echoed. The seeded generator is for reproducible experiments and must not be used for anything security-sensitive. See [SECURITY.md](SECURITY.md) and [docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md).

## Attribution and license

The original script closely resembles Exercise 2 of Chapter 5 ("Iterations") of *Python for Everybody* by Charles Severance ([py4e.com](https://www.py4e.com/html3/05-iterations)), which asks for a program that prints the maximum and minimum of entered numbers. The repository does not record its source, so treat the original program as likely course-derived. The pairwise method is a standard algorithm, described in *Introduction to Algorithms* (Cormen, Leiserson, Rivest, Stein), and its lower bound is due to Ira Pohl (1972).

The repository has no license file, so no open-source license is granted.
