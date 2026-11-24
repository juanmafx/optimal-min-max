# Security Audit

Audit date: 2026-11-23. Scope: the full tree and the complete git history, which is one commit containing one file.

## Findings

| ID | Severity | Finding | Status |
| --- | --- | --- | --- |
| A-1 | Low | Bare `except` also caught interrupts and system exits during parsing | Fixed: only `ValueError` is caught |
| A-2 | Low | Closed standard input ended the program with an unhandled `EOFError` | Fixed: end of input finishes the session |
| A-3 | Low | Input tokens had no explicit length limit | Fixed: limited to 4,096 characters |
| A-4 | Low | The development lock initially resolved a `pytest` version with a published advisory | Fixed: pinned to 9.0.3 |

No findings remain open.

## Checks with no finding

| Area | Result |
| --- | --- |
| Hardcoded secrets, private keys | None in the tree or history |
| Injection, unsafe eval, deserialization | Not present; no `eval`, `exec`, shell, or pickle in application code |
| XSS, CSRF, authentication | Not applicable; no web interface or accounts |
| Weak hashing | Not applicable; no hashing |
| Committed dependencies or build artifacts | None |
| Terminal escape injection | Invalid input is never echoed |

## Supply chain

- The application has no runtime dependencies.
- Development dependencies are pinned with hashes in `uv.lock`.
- `pip-audit` reported no known vulnerabilities in the locked set on the audit date.
- GitHub Actions are pinned to full commit SHAs: `actions/checkout` v7.0.1 and `astral-sh/setup-uv` v10.4.0.
- The workflow has read-only `contents` permission and does not persist checkout credentials.

## Limitations

This was a manual review supported by Ruff security rules, mypy, and `pip-audit`. It was not an independent penetration test. `random.Random` is deliberately used for reproducibility and is not cryptographically secure.
