import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "db" / "schema.sql"
INSERT = (
    "INSERT INTO sample_runs (app_version, seed, lower_bound, upper_bound, sample_count, "
    "minimum_value, maximum_value, comparison_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
)


@pytest.fixture
def connection() -> Iterator[sqlite3.Connection]:
    database = sqlite3.connect(":memory:")
    database.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    yield database
    database.close()


def test_schema_is_idempotent(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def test_valid_run_is_stored(connection: sqlite3.Connection) -> None:
    connection.execute(INSERT, ("1.0.0", "7", "0", "9", 4, "1", "8", 4))
    assert connection.execute("SELECT count(*) FROM sample_runs").fetchone() == (1,)


def test_inconsistent_comparison_count_is_rejected(connection: sqlite3.Connection) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(INSERT, ("1.0.0", "7", "0", "9", 4, "1", "8", 5))


def test_duplicate_run_is_rejected(connection: sqlite3.Connection) -> None:
    connection.execute(INSERT, ("1.0.0", "7", "0", "9", 4, "1", "8", 4))
    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(INSERT, ("1.0.0", "7", "0", "9", 4, "2", "8", 4))
