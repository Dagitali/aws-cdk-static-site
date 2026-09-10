"""
:mod:`scripts.check_release_changelog` module.

Validate that a semantic release version has a corresponding dated section in
the project changelog.
"""

import argparse
import re
from datetime import date
from pathlib import Path

from ._support import REPOSITORY_ROOT, normalize_release, report

# SECTION: FUNCTIONS


def validate(
    changelog: Path,
    release: str,
) -> list[str]:
    """
    Return every release-changelog validation failure.

    Parameters
    ----------
    changelog : pathlib.Path
        Changelog file to inspect.
    release : str
        Semantic version with an optional leading ``v``.

    Returns
    -------
    list[str]
        Human-readable failures; empty when a valid dated section exists.
    """
    try:
        version = normalize_release(release)
    except ValueError as error:
        return [str(error)]

    if not changelog.is_file():
        return [f'changelog does not exist: {changelog}']

    heading_pattern = re.compile(
        rf'^## {re.escape(version)} - (?P<date>\d{{4}}-\d{{2}}-\d{{2}})$',
        re.MULTILINE,
    )
    heading = heading_pattern.search(changelog.read_text(encoding='utf-8'))
    if heading is None:
        return [f'{changelog.name} has no dated section for {version}']

    try:
        date.fromisoformat(heading.group('date'))
    except ValueError:
        return [
            f'{changelog.name} has an invalid date for {version}: '
            f'{heading.group('date')}',
        ]

    return []


def parse_args(
    argv: list[str] | None = None,
) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Parameters
    ----------
    argv : list[str] | None, optional
        Argument list excluding the executable name. Uses ``sys.argv`` when
        omitted.

    Returns
    -------
    argparse.Namespace
        Parsed release version and changelog path.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', help='Release version or tag')
    parser.add_argument(
        '--changelog',
        type=Path,
        default=REPOSITORY_ROOT / 'CHANGELOG.md',
        help='Changelog to validate',
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Run release-changelog validation and return a stable process status.

    Parameters
    ----------
    argv : list[str] | None, optional
        Argument list excluding the executable name.

    Returns
    -------
    int
        Zero when validation succeeds; one when validation fails.
    """
    args = parse_args(argv)
    version = args.release.removeprefix('v')
    return report(
        validate(args.changelog.resolve(), args.release),
        success=f'CHANGELOG.md contains a dated section for {version}',
    )


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    raise SystemExit(main())


# !SECTION
