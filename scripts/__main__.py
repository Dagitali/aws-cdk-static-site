"""
:mod:`scripts.__main__` module.

Command-line interface for repository policy and release-maintenance tools.
"""

import argparse
from collections.abc import Callable
from pathlib import Path
from typing import cast

from ._support import REPOSITORY_ROOT, normalize_release, report
from .check_dependency_boundaries import validate as validate_dependencies
from .check_python_policy import (
    SUPPORTED_PYTHON_SPECIFIER,
)
from .check_python_policy import (
    validate as validate_python,
)
from .check_release_changelog import validate as validate_changelog
from .check_workflow_pins import validate as validate_workflow_pins
from .update_release_snippet import update as update_release_snippet

# SECTION: TYPE ALIASES


type CommandResult = tuple[list[str], str]
type Command = Callable[[argparse.Namespace], CommandResult]


# !SECTION


# SECTION: PROTECTED FUNCTIONS


def _check_dependencies(args: argparse.Namespace) -> CommandResult:
    """
    Validate lowest dependency constraints.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed repository-root option.

    Returns
    -------
    CommandResult
        Failures and success message.
    """
    return (
        validate_dependencies(args.root.resolve()),
        'lowest dependency constraints match pyproject.toml',
    )


def _check_python(args: argparse.Namespace) -> CommandResult:
    """
    Validate the repository's supported Python policy.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed repository-root option.

    Returns
    -------
    CommandResult
        Failures and success message.
    """
    return (
        validate_python(args.root.resolve()),
        f'repository supports Python {SUPPORTED_PYTHON_SPECIFIER}',
    )


def _check_changelog(args: argparse.Namespace) -> CommandResult:
    """
    Validate a versioned changelog section.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed release and changelog options.

    Returns
    -------
    CommandResult
        Failures and success message.
    """
    version = args.release.removeprefix('v')
    return (
        validate_changelog(args.changelog.resolve(), args.release),
        f'CHANGELOG.md contains a dated section for {version}',
    )


def _check_workflows(args: argparse.Namespace) -> CommandResult:
    """
    Validate immutable GitHub Actions references.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed workflow-directory option.

    Returns
    -------
    CommandResult
        Failures and success message.
    """
    workflow_dir = args.workflow_dir.resolve()
    return (
        validate_workflow_pins(workflow_dir),
        f'remote actions are immutably pinned in {workflow_dir}',
    )


def _update_snippet(args: argparse.Namespace) -> CommandResult:
    """
    Update or verify the README release snippet.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed release, README, and check-mode options.

    Returns
    -------
    CommandResult
        Failures and success message.
    """
    try:
        version = normalize_release(args.release)
        failures = update_release_snippet(
            args.readme.resolve(),
            args.release,
            check=args.check,
        )
    except ValueError as error:
        version = args.release.removeprefix('v')
        failures = [str(error)]
    action = 'references' if args.check else 'updated for'
    return failures, f'{args.readme.name} {action} v{version}'


def _add_root_argument(parser: argparse.ArgumentParser) -> None:
    """
    Add the shared repository-root option to a subcommand.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        Subcommand parser to configure.
    """
    parser.add_argument(
        '--root',
        type=Path,
        default=REPOSITORY_ROOT,
        help='Repository root to validate',
    )


# !SECTION


# SECTION: FUNCTIONS


def create_parser() -> argparse.ArgumentParser:
    """
    Create the repository-tools argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Parser containing every supported subcommand and option.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)

    dependency_parser = commands.add_parser(
        'check-dependency-boundaries',
        help='Verify lowest runtime dependency constraints',
    )
    _add_root_argument(dependency_parser)
    dependency_parser.set_defaults(handler=_check_dependencies)

    python_parser = commands.add_parser(
        'check-python-policy',
        help='Verify the supported Python policy',
    )
    _add_root_argument(python_parser)
    python_parser.set_defaults(handler=_check_python)

    changelog_parser = commands.add_parser(
        'check-release-changelog',
        help='Verify a dated release section in the changelog',
    )
    changelog_parser.add_argument('release', help='Release version or tag')
    changelog_parser.add_argument(
        '--changelog',
        type=Path,
        default=REPOSITORY_ROOT / 'CHANGELOG.md',
        help='Changelog to validate',
    )
    changelog_parser.set_defaults(handler=_check_changelog)

    workflow_parser = commands.add_parser(
        'check-workflow-pins',
        help='Verify immutable GitHub Actions references',
    )
    workflow_parser.add_argument(
        '--workflow-dir',
        type=Path,
        default=REPOSITORY_ROOT / '.github' / 'workflows',
        help='Directory containing GitHub Actions workflow files',
    )
    workflow_parser.set_defaults(handler=_check_workflows)

    snippet_parser = commands.add_parser(
        'update-release-snippet',
        help='Update or verify the README release snippet',
    )
    snippet_parser.add_argument('release', help='Release version or tag')
    snippet_parser.add_argument(
        '--check',
        action='store_true',
        help='Check without writing',
    )
    snippet_parser.add_argument(
        '--readme',
        type=Path,
        default=REPOSITORY_ROOT / 'README.md',
        help='README containing the marked installation snippet',
    )
    snippet_parser.set_defaults(handler=_update_snippet)
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run a repository-maintenance subcommand.

    Parameters
    ----------
    argv : list[str] | None, optional
        Argument list excluding the executable name. Uses ``sys.argv`` when
        omitted.

    Returns
    -------
    int
        Conventional status returned by the selected command.
    """
    args = create_parser().parse_args(argv)
    command = cast(Command, args.handler)
    failures, success = command(args)
    return report(failures, success=success)


# !SECTION


# SECTION: MAIN ENTRY POINT


if __name__ == '__main__':
    raise SystemExit(main())


# !SECTION
