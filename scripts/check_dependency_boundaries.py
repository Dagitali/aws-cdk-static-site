"""
:mod:`scripts.check_dependency_boundaries` module.

Validate that lowest-version constraints match runtime dependency metadata.
"""

import re
import tomllib
from pathlib import Path

# SECTION: CONSTANTS


CONSTRAINT_PATTERN = re.compile(
    r'^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)==(?P<version>[^\s]+)$',
)
REQUIREMENT_PATTERN = re.compile(
    r'^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)>=(?P<minimum>[^,\s]+),<[^\s]+$',
)


# !SECTION


# SECTION: PROTECTED FUNCTIONS


def _canonicalize_name(name: str) -> str:
    """
    Normalize a Python distribution name for comparison.

    Parameters
    ----------
    name : str
        Distribution name from metadata or a constraints file.

    Returns
    -------
    str
        Lowercase name with punctuation runs normalized to hyphens.
    """
    return re.sub(r'[-_.]+', '-', name).lower()


def _lowest_metadata_versions(pyproject: Path) -> tuple[dict[str, str], list[str]]:
    """
    Extract lower bounds from canonical runtime dependency metadata.

    Parameters
    ----------
    pyproject : pathlib.Path
        Project metadata file.

    Returns
    -------
    tuple[dict[str, str], list[str]]
        Lowest versions keyed by canonical name and parsing failures.
    """
    metadata = tomllib.loads(pyproject.read_text(encoding='utf-8'))
    dependencies = metadata.get('project', {}).get('dependencies', [])
    versions: dict[str, str] = {}
    failures: list[str] = []
    for requirement in dependencies:
        match = REQUIREMENT_PATTERN.fullmatch(requirement)
        if match is None:
            failures.append(
                'pyproject.toml dependency must declare one lower and upper bound: '
                f'{requirement!r}',
            )
            continue
        name = _canonicalize_name(match.group('name'))
        if name in versions:
            failures.append(f'{pyproject}: duplicate dependency {name!r}')
            continue
        versions[name] = match.group('minimum')
    return versions, failures


def _constraint_versions(constraints: Path) -> tuple[dict[str, str], list[str]]:
    """
    Parse exact versions from the lowest-dependency constraints file.

    Parameters
    ----------
    constraints : pathlib.Path
        Constraints file containing exact runtime dependency versions.

    Returns
    -------
    tuple[dict[str, str], list[str]]
        Exact versions keyed by canonical name and parsing failures.
    """
    versions: dict[str, str] = {}
    failures: list[str] = []
    for line_number, raw_line in enumerate(
        constraints.read_text(encoding='utf-8').splitlines(),
        start=1,
    ):
        line = raw_line.split('#', maxsplit=1)[0].strip()
        if not line:
            continue
        match = CONSTRAINT_PATTERN.fullmatch(line)
        if match is None:
            failures.append(
                f'{constraints}:{line_number}: expected name==version; '
                f'received {line!r}',
            )
            continue
        name = _canonicalize_name(match.group('name'))
        if name in versions:
            failures.append(
                f'{constraints}:{line_number}: duplicate constraint {name!r}',
            )
            continue
        versions[name] = match.group('version')
    return versions, failures


# !SECTION


# SECTION: FUNCTIONS


def validate(root: Path) -> list[str]:
    """
    Return every dependency-boundary policy violation.

    Parameters
    ----------
    root : pathlib.Path
        Repository root containing metadata and lowest constraints.

    Returns
    -------
    list[str]
        Human-readable violations; empty when both definitions agree.
    """
    pyproject = root / 'pyproject.toml'
    constraints = root / 'requirements' / 'lowest.txt'
    missing = [path for path in (pyproject, constraints) if not path.is_file()]
    if missing:
        return [
            f'required dependency-boundary file does not exist: {path}'
            for path in missing
        ]

    expected, failures = _lowest_metadata_versions(pyproject)
    actual, constraint_failures = _constraint_versions(constraints)
    failures.extend(constraint_failures)
    if not failures and expected != actual:
        failures.append(
            f'{constraints.relative_to(root)}: expected {expected!r}; '
            f'received {actual!r}',
        )
    return failures


# !SECTION
