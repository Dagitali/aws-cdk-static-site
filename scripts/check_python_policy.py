#!/usr/bin/env python3
"""
:mod:`scripts.check_python_policy` module.

Validate that package metadata, development commands, and GitHub Actions agree
on the repository's supported Python-version range.
"""

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


def _is_supported_python(
    version: tuple[int, int],
) -> bool:
    """
    Return whether a Python version satisfies the support interval.

    Parameters
    ----------
    version : tuple[int, int]
        Python major and minor version.

    Returns
    -------
    bool
        ``True`` when *version* is supported; otherwise, ``False``.
    """
    return MINIMUM_PYTHON <= version < MAXIMUM_PYTHON


def _normalize_yaml_scalar(
    value: str,
) -> str:
    """
    Remove YAML quoting, surrounding whitespace, and an inline comment.

    Parameters
    ----------
    value : str
        Raw scalar text extracted from a workflow.

    Returns
    -------
    str
        Normalized scalar value.
    """
    value = value.split(' #', maxsplit=1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_python_version(
    value: str,
) -> tuple[int, int] | None:
    """
    Parse a ``major.minor`` Python version.

    Parameters
    ----------
    value : str
        Candidate version text.

    Returns
    -------
    tuple[int, int] | None
        Parsed major and minor components, or ``None`` when invalid.
    """
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
    """
    Record a mismatch between an actual and expected policy value.

    Parameters
    ----------
    failures : list[str]
        Mutable collection of validation failures.
    actual : object
        Value read from repository configuration.
    expected : object
        Required policy value.
    location : str
        Human-readable configuration location.
    """
    if actual != expected:
        failures.append(f'{location}: expected {expected!r}, received {actual!r}')


def _resolve_workflow_versions(
    value: str,
    content: str,
) -> tuple[str, ...]:
    """
    Resolve a workflow version literal, environment value, or matrix list.

    Parameters
    ----------
    value : str
        Literal scalar or ``env`` expression.
    content : str
        Complete workflow source containing the environment declaration.

    Returns
    -------
    tuple[str, ...]
        Resolved version values, or the original value when an expression
        cannot be resolved.
    """
    env_match = re.fullmatch(r'\$\{\{\s*env\.([A-Z][A-Z0-9_]*)\s*}}', value)
    if env_match is not None:
        name = re.escape(env_match.group(1))
        declaration = re.search(
            rf'^  {name}:[ \t]*(.+?)[ \t]*$',
            content,
            re.MULTILINE,
        )
        if declaration is not None:
            return (_normalize_yaml_scalar(declaration.group(1)),)

    matrix_match = re.fullmatch(
        r'\$\{\{\s*matrix\.([A-Za-z][A-Za-z0-9_-]*)\s*}}',
        value,
    )
    if matrix_match is not None:
        name = re.escape(matrix_match.group(1))
        declaration = re.search(
            rf'^[ \t]+{name}:[ \t]*$'
            rf'(?P<items>(?:\n[ \t]+-[ \t]+[^\n]+)+)',
            content,
            re.MULTILINE,
        )
        if declaration is not None:
            values = re.findall(
                r'^[ \t]+-[ \t]+(.+?)[ \t]*$',
                declaration.group('items'),
                re.MULTILINE,
            )
            return tuple(_normalize_yaml_scalar(item) for item in values)

    return (value,)


# !SECTION


# SECTION: FUNCTIONS


def validate(
    root: Path,
    *,
    running_python: tuple[int, int] | None = None,
) -> list[str]:
    """
    Return every repository Python-policy violation.

    Parameters
    ----------
    root : pathlib.Path
        Repository root containing project and automation configuration.
    running_python : tuple[int, int] | None, optional
        Python version to validate instead of the active interpreter.

    Returns
    -------
    list[str]
        Human-readable policy violations; empty when the policy is satisfied.
    """
    if not root.is_dir():
        return [f'repository root does not exist: {root}']

    failures: list[str] = []
    version = running_python or sys.version_info[:2]
    if not _is_supported_python(version):
        failures.append(
            'checker runtime: Python '
            f'{SUPPORTED_PYTHON_SPECIFIER} is required; '
            f'received {version[0]}.{version[1]}',
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
            location=f'pyproject.toml {location}',
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
    policy_hook = re.search(
        r'^\s*- id: check-python-policy\s*$'
        r'.*?^\s+entry: python scripts/check_python_policy\.py\s*$'
        r'.*?^\s+language: python\s*$',
        pre_commit,
        re.MULTILINE | re.DOTALL,
    )
    if policy_hook is None:
        failures.append(
            '.pre-commit-config.yaml: Python policy hook must use managed Python',
        )

    makefile = (root / 'Makefile').read_text(encoding='utf-8')
    make_requirements = (
        'PY ?= python3',
        'MINIMUM_PYTHON_VERSION ?= 3.13',
        'MAXIMUM_PYTHON_VERSION ?= 3.15',
        'python-policy:',
    )
    for expected in make_requirements:
        if expected not in makefile:
            failures.append(f'Makefile: missing {expected!r}')

    version_pattern = re.compile(
        r'^[ \t]*python-version:[ \t]*(.+?)[ \t]*$',
        re.MULTILINE,
    )
    workflow_dir = root / '.github' / 'workflows'
    for path in sorted((*workflow_dir.glob('*.yml'), *workflow_dir.glob('*.yaml'))):
        content = path.read_text(encoding='utf-8')
        configured_versions = [
            resolved
            for value in version_pattern.findall(content)
            for resolved in _resolve_workflow_versions(
                _normalize_yaml_scalar(value),
                content,
            )
        ]
        for configured_version in configured_versions:
            parsed_version = _parse_python_version(configured_version)
            if parsed_version is None or not _is_supported_python(parsed_version):
                failures.append(
                    f'{path.relative_to(root)}: unsupported Python version '
                    f'{configured_version!r}',
                )
        if 'actions/setup-python@' in content and not configured_versions:
            failures.append(
                f'{path.relative_to(root)}: setup-python requires an explicit '
                f'{MINIMUM_PYTHON_TEXT} version',
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
        Parsed repository-root option.
    """
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--root',
        type=Path,
        default=root,
        help='Repository root to validate',
    )
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
) -> int:
    """
    Run Python-policy checks and return a stable process status.

    Parameters
    ----------
    argv : list[str] | None, optional
        Argument list excluding the executable name.

    Returns
    -------
    int
        Zero when validation succeeds; one when violations are found.
    """
    args = parse_args(argv)
    failures = validate(args.root.resolve())
    if failures:
        for failure in failures:
            print(f'FAIL: {failure}')
        return 1
    print(f'PASS: repository supports Python {SUPPORTED_PYTHON_SPECIFIER}')
    return 0


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    sys.exit(main())


# !SECTION
