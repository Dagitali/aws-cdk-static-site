#!/usr/bin/env python3
"""Verify that a release version has a dated changelog section."""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# SECTION: CONSTANTS


RELEASE_VERSION_PATTERN = re.compile(
    r'^v?(?P<version>(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))$',
)


# !SECTION


# SECTION: FUNCTIONS


def validate(
    changelog: Path,
    release: str,
) -> list[str]:
    """Return every release-changelog validation failure."""
    match = RELEASE_VERSION_PATTERN.fullmatch(release)
    if match is None:
        return [
            'release version must use vMAJOR.MINOR.PATCH or '
            f"MAJOR.MINOR.PATCH: {release!r}",
        ]

    if not changelog.is_file():
        return [f"changelog does not exist: {changelog}"]

    version = match.group('version')
    heading_pattern = re.compile(
        rf"^## {re.escape(version)} - (?P<date>\d{{4}}-\d{{2}}-\d{{2}})$",
        re.MULTILINE,
    )
    heading = heading_pattern.search(changelog.read_text(encoding='utf-8'))
    if heading is None:
        return [f"{changelog.name} has no dated section for {version}"]

    try:
        date.fromisoformat(heading.group('date'))
    except ValueError:
        return [
            f"{changelog.name} has an invalid date for {version}: "
            f"{heading.group('date')}",
        ]

    return []


def parse_args(
    argv: list[str] | None = None,
) -> argparse.Namespace:
    """Parse command-line arguments."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', help='Release version or tag')
    parser.add_argument(
        '--changelog',
        type=Path,
        default=root / 'CHANGELOG.md',
        help='Changelog to validate',
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
) -> int:
    """Run release-changelog validation and return a stable process status."""
    args = parse_args(argv)
    failures = validate(args.changelog.resolve(), args.release)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    version = args.release.removeprefix('v')
    print(f"PASS: CHANGELOG.md contains a dated section for {version}")
    return 0


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    sys.exit(main())


# !SECTION
