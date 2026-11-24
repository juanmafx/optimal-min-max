-- Optional SQLite schema for storing sample run results; the application never requires it.
-- Extrema are decimal TEXT because Python integers are unbounded and SQLite INTEGER is 64-bit.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sample_runs (
    run_id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    app_version TEXT NOT NULL CHECK (length(app_version) BETWEEN 1 AND 32),
    seed TEXT NOT NULL CHECK (length(seed) BETWEEN 1 AND 4096),
    lower_bound TEXT NOT NULL CHECK (length(lower_bound) BETWEEN 1 AND 4096),
    upper_bound TEXT NOT NULL CHECK (length(upper_bound) BETWEEN 1 AND 4096),
    sample_count INTEGER NOT NULL CHECK (sample_count BETWEEN 1 AND 10000000),
    minimum_value TEXT NOT NULL CHECK (length(minimum_value) BETWEEN 1 AND 4096),
    maximum_value TEXT NOT NULL CHECK (length(maximum_value) BETWEEN 1 AND 4096),
    comparison_count INTEGER NOT NULL,
    CHECK (comparison_count = (3 * sample_count + 1) / 2 - 2),
    UNIQUE (app_version, seed, lower_bound, upper_bound, sample_count)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_sample_runs_created_at ON sample_runs (created_at);
