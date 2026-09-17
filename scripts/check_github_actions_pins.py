"""
:mod:`scripts.check_github_actions_pins` module.

Validate that every remote GitHub Action reference in workflows and composite
actions uses an immutable, full-length commit SHA.
"""

import re
from pathlib import Path

from ._support import workflow_paths

# SECTION: CONSTANTS


FULL_COMMIT_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')
USES_PATTERN = re.compile(
    r"^\s*(?:-\s*)?uses:\s*[\"']?([^\s\"']+)[\"']?\s*(?:#.*)?$",
)


# !SECTION


# SECTION: FUNCTIONS


def validate(
    automation_dir: Path,
) -> list[str]:
    """
    Return every mutable or malformed remote action reference.

    Parameters
    ----------
    automation_dir : pathlib.Path
        Directory tree containing GitHub Actions workflow and action YAML.

    Returns
    -------
    list[str]
        Human-readable failures; empty when every remote action is pinned.
    """
    if not automation_dir.is_dir():
        return [f'automation directory does not exist: {automation_dir}']

    failures: list[str] = []
    for path in workflow_paths(automation_dir):
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
                    f'{path}:{line_number}: remote action must use a full '
                    f'40-character commit SHA: {reference}',
                )
    return failures


# !SECTION
