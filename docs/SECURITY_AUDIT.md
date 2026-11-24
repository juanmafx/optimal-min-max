# Security Audit

Audit dates: 2026-11-23 and 2026-11-24. Scope: the full tree and the complete git history of the `modernize/2026` branch.

## Findings

| ID | Severity | Finding | Status |
| --- | --- | --- | --- |
| A-1 | Low | Bare `except` also caught interrupts and system exits during parsing | Fixed: only `ValueError` is caught |
| A-2 | Low | Closed standard input ended the program with an unhandled `EOFError` | Fixed: end of input finishes the session |
| A-3 | Low | Input tokens had no explicit length limit | Fixed: limited to 4,096 characters |
| A-4 | Low | The development lock initially resolved a `pytest` version with a published advisory | Fixed: pinned to 9.0.3 |
| A-5 | Medium | A long line without a newline was read fully into memory before the length check; a 200 MB line used about 409 MB | Fixed: piped input is read in bounded chunks, measured at about 17 MB for the same line |
| A-6 | Low | Undecodable input bytes ended the session with a traceback | Fixed: reported as invalid input |
| A-7 | Low | `sample` bounds and seed accepted values longer than the schema can store | Fixed: limited to 4,096 characters |
| A-8 | Low | Seeds `n` and `-n` produced identical samples while being recorded as different runs | Fixed: negative seeds are rejected |

No findings remain open.

## Checks with no finding

| Area | Result |
| --- | --- |
| Hardcoded secrets, private keys | None in the tree or history, confirmed with `gitleaks` |
| Injection, unsafe eval, deserialization | Not present; no `eval`, `exec`, shell, or pickle in application code |
| XSS, CSRF, authentication | Not applicable; no web interface or accounts |
| Weak hashing | Not applicable; no hashing |
| Committed dependencies or build artifacts | None |
| Terminal escape injection | Invalid interactive input and rejected numeric options are never echoed |

## Supply chain

- The application has no runtime dependencies.
- Development dependencies are pinned with hashes in `uv.lock`.
- The build backend `hatchling` is pinned by version in `pyproject.toml`, but it and its dependencies are not hash-locked.
- `pip-audit` reported no known vulnerabilities in the locked set or the resolved build backend set on 2026-11-24.
- GitHub Actions are pinned to full commit SHAs: `actions/checkout` v7.0.1 and `astral-sh/setup-uv` v10.4.0.
- The workflow has read-only `contents` permission and does not persist checkout credentials.

## Limitations

This was a manual review supported by Ruff security rules, mypy, `pip-audit`, and `gitleaks`. It was not an independent penetration test. `random.Random` is deliberately used for reproducibility and is not cryptographically secure.
