import argparse
import io
import json
import sys
from collections.abc import Callable, Sequence

from py_low_hig import __version__
from py_low_hig.cli.line_reader import bounded_line_reader
from py_low_hig.cli.session import run_session
from py_low_hig.core.bounds import baseline_comparisons
from py_low_hig.core.extrema import find_extrema
from py_low_hig.parsing.tokens import MAX_TOKEN_LENGTH, parse_integer
from py_low_hig.sampling.uniform import uniform_integers

MAX_SAMPLE_COUNT = 10_000_000
INTERRUPTED_EXIT_CODE = 130


def _bounded_integer(raw: str) -> int:
    value = parse_integer(raw)
    if value is None:
        raise argparse.ArgumentTypeError(
            f"must be an integer of at most {MAX_TOKEN_LENGTH} characters"
        )
    return value


def _seed(raw: str) -> int:
    value = _bounded_integer(raw)
    if value < 0:
        raise argparse.ArgumentTypeError("must not be negative")
    return value


def _sample_count(raw: str) -> int:
    count = _bounded_integer(raw)
    if not 1 <= count <= MAX_SAMPLE_COUNT:
        raise argparse.ArgumentTypeError(f"must be between 1 and {MAX_SAMPLE_COUNT}")
    return count


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py-low-hig",
        description="Find the minimum and maximum of integers with optimal comparisons.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("interactive", help="read integers until 'done' (default)")
    sample = commands.add_parser("sample", help="analyze a reproducible uniform integer sample")
    sample.add_argument("--count", type=_sample_count, required=True)
    sample.add_argument("--low", type=_bounded_integer, default=0)
    sample.add_argument("--high", type=_bounded_integer, default=1_000_000)
    sample.add_argument("--seed", type=_seed, default=0)
    sample.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _line_reader() -> Callable[[str], str]:
    if isinstance(sys.stdin, io.TextIOWrapper):
        sys.stdin.reconfigure(errors="replace")
    if sys.stdin.isatty():
        return input
    return bounded_line_reader(sys.stdin, sys.stdout)


def _run_interactive() -> int:
    try:
        run_session(_line_reader(), print)
    except KeyboardInterrupt:
        print(file=sys.stderr)
        return INTERRUPTED_EXIT_CODE
    return 0


def _run_sample(args: argparse.Namespace) -> int:
    result = find_extrema(uniform_integers(args.count, args.low, args.high, args.seed))
    if result is None:
        raise RuntimeError("sample produced no values")
    report = {
        "seed": args.seed,
        "low": args.low,
        "high": args.high,
        "count": result.count,
        "minimum": result.minimum,
        "maximum": result.maximum,
        "comparisons": result.comparisons,
        "baseline_comparisons": baseline_comparisons(result.count),
    }
    if args.as_json:
        print(json.dumps(report, sort_keys=True))
    else:
        for key, value in report.items():
            print(f"{key}: {value}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "sample":
        if args.low > args.high:
            parser.error("--low must not exceed --high")
        return _run_sample(args)
    return _run_interactive()
