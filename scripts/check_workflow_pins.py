"""
:mod:`scripts.check_workflow_pins` module.

Validate that every remote GitHub Action reference uses an immutable,
full-length commit SHA.
"""

import argparse
import re
from pathlib import Path

from ._support import REPOSITORY_ROOT, report, workflow_paths

# SECTION: CONSTANTS


FULL_COMMIT_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')
USES_PATTERN = re.compile(
    r"^\s*(?:-\s*)?uses:\s*[\"']?([^\s\"']+)[\"']?\s*(?:#.*)?$",
)


# !SECTION


# SECTION: FUNCTIONS


def validate(
    workflow_dir: Path,
) -> list[str]:
    """
    Return every mutable or malformed remote action reference.

    Parameters
    ----------
    workflow_dir : pathlib.Path
        Directory containing GitHub Actions YAML files.

    Returns
    -------
    list[str]
        Human-readable failures; empty when every remote action is pinned.
    """
    if not workflow_dir.is_dir():
        return [f'workflow directory does not exist: {workflow_dir}']

    failures: list[str] = []
    for path in workflow_paths(workflow_dir):
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
        Parsed workflow-directory option.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--workflow-dir',
        type=Path,
        default=REPOSITORY_ROOT / '.github' / 'workflows',
        help='Directory containing GitHub Actions workflow files',
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Run workflow-pin validation and return a stable process status.

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
    workflow_dir = args.workflow_dir.resolve()
    return report(
        validate(workflow_dir),
        success=f'remote actions are immutably pinned in {workflow_dir}',
    )


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    raise SystemExit(main())

# !SECTION
