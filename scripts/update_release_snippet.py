#!/usr/bin/env python3
"""
:mod:`scripts.update_release_snippet` module.

Render, update, or verify the README installation snippet associated with a
semantic release tag.
"""

import argparse
import re
import sys
from pathlib import Path

# SECTION: CONSTANTS


END_MARKER = '<!-- release-install:end -->'
RELEASE_PATTERN = re.compile(
    r'^v?(?P<version>(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))$',
)
START_MARKER = '<!-- release-install:start -->'


# !SECTION


# SECTION: FUNCTIONS


def render(
    release: str,
) -> str:
    """
    Render the complete marked installation snippet for a release.

    Parameters
    ----------
    release : str
        Semantic version with an optional leading ``v``.

    Returns
    -------
    str
        Markdown marker pair and installation command for the normalized tag.

    Raises
    ------
    ValueError
        If *release* is not a semantic ``major.minor.patch`` version.
    """
    match = RELEASE_PATTERN.fullmatch(release)
    if match is None:
        raise ValueError(
            'release version must use vMAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH: '
            f'{release!r}',
        )
    tag = f'v{match.group('version')}'
    return (
        f'{START_MARKER}\n'
        '```bash\n'
        'python -m pip install \\\n'
        '  "aws-cdk-static-site @ '
        'git+https://github.com/Dagitali/aws-cdk-static-site.git@'
        f'{tag}"\n'
        '```\n'
        f'{END_MARKER}'
    )


def update(
    readme: Path,
    release: str,
    *,
    check: bool = False,
) -> list[str]:
    """
    Update the marked snippet or return validation failures in check mode.

    Parameters
    ----------
    readme : pathlib.Path
        README containing one release-installation marker pair.
    release : str
        Semantic version with an optional leading ``v``.
    check : bool, optional
        Validate existing content without writing when ``True``.

    Returns
    -------
    list[str]
        Human-readable failures; empty after a successful update or check.

    Raises
    ------
    ValueError
        If *release* is not a semantic ``major.minor.patch`` version.
    """
    if not readme.is_file():
        return [f'readme does not exist: {readme}']

    content = readme.read_text(encoding='utf-8')
    if content.count(START_MARKER) != 1 or content.count(END_MARKER) != 1:
        return [f'{readme.name} must contain one release installation marker pair']

    start = content.index(START_MARKER)
    end = content.index(END_MARKER, start) + len(END_MARKER)
    expected = render(release)
    if content[start:end] == expected:
        return []
    if check:
        tag = release if release.startswith('v') else f'v{release}'
        return [f'{readme.name} installation snippet does not reference {tag}']

    readme.write_text(
        f'{content[:start]}{expected}{content[end:]}',
        encoding='utf-8',
    )
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
        Parsed release, mode, and README path.
    """
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', help='Release version or tag')
    parser.add_argument('--check', action='store_true', help='Check without writing')
    parser.add_argument(
        '--readme',
        type=Path,
        default=root / 'README.md',
        help='README containing the marked installation snippet',
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Update or verify the release installation snippet.

    Parameters
    ----------
    argv : list[str] | None, optional
        Argument list excluding the executable name.

    Returns
    -------
    int
        Zero when the update or check succeeds; one when validation fails.
    """
    args = parse_args(argv)
    try:
        failures = update(args.readme.resolve(), args.release, check=args.check)
    except ValueError as error:
        failures = [str(error)]
    if failures:
        for failure in failures:
            print(f'FAIL: {failure}')
        return 1

    action = 'references' if args.check else 'updated for'
    tag = args.release if args.release.startswith('v') else f'v{args.release}'
    print(f'PASS: {args.readme.name} {action} {tag}')
    return 0


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    sys.exit(main())


# !SECTION
