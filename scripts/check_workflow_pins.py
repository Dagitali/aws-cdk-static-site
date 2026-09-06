#!/usr/bin/env python3
"""Verify that remote GitHub Actions use immutable commit references."""

import argparse
import re
import sys
from pathlib import Path

# SECTION: CONSTANTS


FULL_COMMIT_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')
USES_PATTERN = re.compile(
    r"^\s*(?:-\s*)?uses:\s*[\"']?([^\s\"']+)[\"']?\s*(?:#.*)?$",
)


# !SECTION


# SECTION: FUNCTIONS


def validate(workflow_dir: Path) -> list[str]:
    """Return every mutable or malformed remote action reference."""
    if not workflow_dir.is_dir():
        return [f"workflow directory does not exist: {workflow_dir}"]

    failures: list[str] = []
    paths = (*workflow_dir.glob('*.yml'), *workflow_dir.glob('*.yaml'))
    for path in sorted(paths):
        lines = path.read_text(encoding='utf-8').splitlines()
        for line_number, line in enumerate(lines, start=1):
            match = USES_PATTERN.match(line)
            if match is None:
                continue
            reference = match.group(1)
            if reference.startswith(('./', 'docker://')):
                continue
            action, separator, revision = reference.rpartition('@')
            if (
                not separator
                or not action
                or not FULL_COMMIT_PATTERN.fullmatch(revision)
            ):
                failures.append(
                    f"{path}:{line_number}: remote action must use a full "
                    f"40-character commit SHA: {reference}",
                )
    return failures


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--workflow-dir',
        type=Path,
        default=root / '.github' / 'workflows',
        help='Directory containing GitHub Actions workflow files',
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run workflow pin validation and return a stable process status."""
    args = parse_args(argv)
    workflow_dir = args.workflow_dir.resolve()
    failures = validate(workflow_dir)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: remote actions are immutably pinned in {workflow_dir}")
    return 0


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    sys.exit(main())

# !SECTION
