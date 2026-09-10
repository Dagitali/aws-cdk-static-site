"""
:mod:`scripts.check_release_changelog` module.

Validate that a semantic release version has a corresponding dated section in
the project changelog.
"""

import re
from datetime import date
from pathlib import Path

from ._support import normalize_release

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


# !SECTION
