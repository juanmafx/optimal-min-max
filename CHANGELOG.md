# Changelog

This project follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - Unreleased

First versioned release, prepared on 2026-11-23.

### Added

- Installable `py-low-hig` command and typed library API.
- Streaming extrema tracker using the optimal `ceil(3n / 2) - 2` comparisons.
- Seeded `sample` command with text and JSON output.
- Unit, property-based, statistical, schema, and end-to-end tests with a committed report.
- Optional SQLite schema, architecture and security documentation, and CI.

### Changed

- **Breaking:** `hi_low.py` is replaced by `py-low-hig` and `python -m py_low_hig`.
- **Breaking:** a session with no valid numbers prints `No numbers were entered.` instead of `Maximum is None` and `Minimum is None`.
- Closed standard input now finishes the session instead of raising `EOFError`.

### Security

- Replaced the bare `except` with a specific `ValueError` handler.
- Limited input tokens to 4,096 characters.

## Original script - 2019

Single-file exercise, unversioned.
