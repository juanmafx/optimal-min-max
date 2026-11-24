# Changelog

This project follows [Semantic Versioning](https://semver.org/).

## [1.0.1] - 2026-11-24

### Changed

- Documentation corrections: the release notes and changelog now reflect the published 1.0.0 release. No code behaviour change.

## [1.0.0] - 2026-11-24

First versioned release.

### Added

- Installable `py-low-hig` command and typed library API.
- Streaming extrema tracker using the optimal `ceil(3n / 2) - 2` comparisons.
- Seeded `sample` command with text and JSON output.
- Unit, property-based, statistical, schema, and end-to-end tests with a committed report.
- Optional SQLite schema, architecture and security documentation, and CI.

### Changed

- **Breaking:** `hi_low.py` is replaced by `py-low-hig` and `python -m py_low_hig`.
- **Breaking:** a session with no valid numbers prints `No numbers were entered.` instead of `Maximum is None` and `Minimum is None`.
- **Breaking:** input tokens longer than 4,096 characters are invalid, including integers the original script accepted.
- Closed standard input now finishes the session instead of raising `EOFError`.
- Undecodable input bytes are reported as invalid instead of ending the session with a traceback.
- `sample` rejects negative seeds, because Python seeds `n` and `-n` produce the same stream.

### Security

- Replaced the bare `except` with a specific `ValueError` handler.
- Limited input tokens and numeric `sample` options to 4,096 characters.
- Piped input is read in bounded chunks, so oversized lines no longer grow memory use.

## Original script - 2019

Single-file exercise, unversioned.
