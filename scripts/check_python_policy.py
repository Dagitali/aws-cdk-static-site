#!/usr/bin/env python3
"""Verify the repository-wide supported Python version policy."""

import argparse
import re
import sys
import tomllib
from pathlib import Path

# SECTION: CONSTANTS


MAXIMUM_PYTHON = (3, 15)
MINIMUM_PYTHON = (3, 13)
MINIMUM_PYTHON_TEXT = '3.13'
SUPPORTED_PYTHON_SPECIFIER = '>=3.13,<3.15'


# !SECTION


# SECTION: PROTECTED FUNCTIONS


def _is_supported_python(version: tuple[int, int]) -> bool:
    return MINIMUM_PYTHON <= version < MAXIMUM_PYTHON


def _normalize_yaml_scalar(
    value: str,
) -> str:
    value = value.split(' #', maxsplit=1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_python_version(
    value: str,
) -> tuple[int, int] | None:
    match = re.fullmatch(r'(\d+)\.(\d+)', value)
    if match is None:
        return None
    return int(match.group(1)), int(match.group(2))


def _require_value(
    failures: list[str],
    *,
    actual: object,
    expected: object,
    location: str,
) -> None:
    if actual != expected:
        failures.append(f"{location}: expected {expected!r}, received {actual!r}")


def _resolve_workflow_env(
    value: str,
    content: str,
) -> str:
    match = re.fullmatch(r'\$\{\{\s*env\.([A-Z][A-Z0-9_]*)\s*}}', value)
    if match is None:
        return value

    name = re.escape(match.group(1))
    declaration = re.search(
        rf'^  {name}:\s*(.+?)\s*$',
        content,
        re.MULTILINE,
    )
    if declaration is None:
        return value
    return _normalize_yaml_scalar(declaration.group(1))


# !SECTION


# SECTION: FUNCTIONS


def validate(
    root: Path,
    *,
    running_python: tuple[int, int] | None = None,
) -> list[str]:
    """Return every repository Python-policy violation."""
    if not root.is_dir():
        return [f"repository root does not exist: {root}"]

    failures: list[str] = []
    version = running_python or sys.version_info[:2]
    if not _is_supported_python(version):
        failures.append(
            'checker runtime: Python '
            f"{SUPPORTED_PYTHON_SPECIFIER} is required; "
            f"received {version[0]}.{version[1]}",
        )

    pyproject = tomllib.loads((root / 'pyproject.toml').read_text(encoding='utf-8'))
    expected_values = (
        (
            pyproject['project']['requires-python'],
            SUPPORTED_PYTHON_SPECIFIER,
            'project.requires-python',
        ),
        (
            pyproject['tool']['mypy']['python_version'],
            '3.13',
            'tool.mypy.python_version',
        ),
        (
            pyproject['tool']['ruff']['target-version'],
            'py313',
            'tool.ruff.target-version',
        ),
    )
    for actual, expected, location in expected_values:
        _require_value(
            failures,
            actual=actual,
            expected=expected,
            location=f"pyproject.toml {location}",
        )

    _require_value(
        failures,
        actual=(root / '.python-version').read_text(encoding='utf-8').strip(),
        expected=MINIMUM_PYTHON_TEXT,
        location='.python-version',
    )

    pre_commit = (root / '.pre-commit-config.yaml').read_text(encoding='utf-8')
    if re.search(r'^\s*python:\s*python3\s*$', pre_commit, re.MULTILINE) is None:
        failures.append('.pre-commit-config.yaml: default Python must be python3')
    if 'entry: python3 scripts/check_python_policy.py' not in pre_commit:
        failures.append('.pre-commit-config.yaml: Python policy hook is missing')

    makefile = (root / 'Makefile').read_text(encoding='utf-8')
    make_requirements = (
        'PY ?= python3',
        'MINIMUM_PYTHON_VERSION ?= 3.13',
        'MAXIMUM_PYTHON_VERSION ?= 3.15',
        'python-policy:',
    )
    for expected in make_requirements:
        if expected not in makefile:
            failures.append(f"Makefile: missing {expected!r}")

    version_pattern = re.compile(r'^\s*python-version:\s*(.+?)\s*$', re.MULTILINE)
    workflow_dir = root / '.github' / 'workflows'
    for path in sorted((*workflow_dir.glob('*.yml'), *workflow_dir.glob('*.yaml'))):
        content = path.read_text(encoding='utf-8')
        configured_versions = [
            _resolve_workflow_env(_normalize_yaml_scalar(value), content)
            for value in version_pattern.findall(content)
        ]
        for configured_version in configured_versions:
            parsed_version = _parse_python_version(configured_version)
            if parsed_version is None or not _is_supported_python(parsed_version):
                failures.append(
                    f"{path.relative_to(root)}: unsupported Python version "
                    f"{configured_version!r}",
                )
        if 'actions/setup-python@' in content and not configured_versions:
            failures.append(
                f"{path.relative_to(root)}: setup-python requires an explicit "
                f"{MINIMUM_PYTHON_TEXT} version",
            )

    return failures


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root',
        type=Path,
        default=root,
        help='Repository root to validate',
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run Python-policy checks and return a stable process status."""
    args = parse_args(argv)
    failures = validate(args.root.resolve())
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print(f"PASS: repository supports Python {SUPPORTED_PYTHON_SPECIFIER}")
    return 0


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    sys.exit(main())


# !SECTION
