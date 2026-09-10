"""
:mod:`scripts._support` module.

Shared, private support for repository-maintenance commands.
"""

import re
from collections.abc import Sequence
from pathlib import Path

# SECTION: CONSTANTS


RELEASE_PATTERN = re.compile(
    r'^v?(?P<version>(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*))$',
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


# !SECTION


# SECTION: FUNCTIONS


def normalize_release(release: str, /) -> str:
    """
    Return a normalized semantic release version.

    Parameters
    ----------
    release : str
        Semantic version with an optional leading ``v``.

    Returns
    -------
    str
        Semantic version without a leading ``v``.

    Raises
    ------
    ValueError
        If *release* is not a semantic ``major.minor.patch`` version.
    """
    if match := RELEASE_PATTERN.fullmatch(release):
        return match.group('version')
    raise ValueError(
        'release version must use vMAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH: '
        f'{release!r}',
    )


def report(failures: Sequence[str], /, *, success: str) -> int:
    """
    Print command results and return their conventional process status.

    Parameters
    ----------
    failures : collections.abc.Sequence[str]
        Validation failures to report.
    success : str
        Message to print when no failures exist.

    Returns
    -------
    int
        One when failures exist; otherwise, zero.
    """
    if failures:
        for failure in failures:
            print(f'FAIL: {failure}')
        return 1
    print(f'PASS: {success}')
    return 0


def workflow_paths(directory: Path, /) -> list[Path]:
    """
    Return sorted YAML workflow paths from a directory.

    Parameters
    ----------
    directory : pathlib.Path
        Directory containing GitHub Actions workflow files.

    Returns
    -------
    list[pathlib.Path]
        Sorted ``.yml`` and ``.yaml`` paths.
    """
    return sorted((*directory.glob('*.yml'), *directory.glob('*.yaml')))


# !SECTION
