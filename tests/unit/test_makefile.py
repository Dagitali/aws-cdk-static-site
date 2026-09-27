"""
:mod:`tests.unit.test_makefile` module.

Contract tests for repository-maintenance Make targets and safety boundaries.
"""

import os
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

# SECTION: TYPE ALIASES


type MakeRunner = Callable[..., subprocess.CompletedProcess[str]]


# !SECTION


# SECTION: FIXTURES


@pytest.fixture
def make(
    repository_root: Path,
    tmp_path: Path,
) -> MakeRunner:
    """Run Make in a disposable checkout without inherited flags or local overrides."""
    executable = shutil.which('make')
    if executable is None:
        pytest.skip('Make contract tests require make')
    checkout = tmp_path / 'checkout'
    checkout.mkdir()
    shutil.copyfile(repository_root / 'Makefile', checkout / 'Makefile')
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {'MAKEFLAGS', 'MFLAGS', 'MAKELEVEL', 'MAKEOVERRIDES', 'MAKEFILES'}
    }

    def run(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            (executable, 'ENV_FILE=', 'SHARED_MAKEFILE=', *arguments),
            cwd=checkout,
            env=environment,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )

    return run


# !SECTION


# SECTION: TESTS


class TestMakefileContracts:
    """Verify overridable commands and destructive-operation safeguards."""

    @pytest.mark.parametrize(
        ('variable', 'safe_overrides'),
        (
            ('CLEAN_REMOVE_PATHS', ()),
            (
                'CLEAN_SEARCH_DIRS',
                ('CLEAN_REMOVE_PATHS=.test-clean-placeholder',),
            ),
        ),
    )
    def test_clean_rejects_paths_outside_repository(
        self,
        make: MakeRunner,
        tmp_path: Path,
        variable: str,
        safe_overrides: tuple[str, ...],
    ) -> None:
        result = make('clean', *safe_overrides, f'{variable}={tmp_path}')

        assert result.returncode != 0
        assert f'{variable} must be' in result.stderr
        assert tmp_path.is_dir()

    @pytest.mark.parametrize(
        ('arguments', 'expected_output'),
        [
            pytest.param(
                (
                    'install',
                    'VENV_READY_COMMAND=printf venv-ready',
                    'RUNTIME_INSTALL_COMMAND=printf runtime-install',
                    'RUNTIME_POST_INSTALL_COMMAND=printf runtime-post-install',
                ),
                (
                    'printf venv-ready',
                    'printf runtime-install',
                    'printf runtime-post-install',
                ),
                id='installation',
            ),
            pytest.param(
                (
                    'format-check',
                    'test-unit',
                    'PYTHON_FORMAT_PATHS=example.py',
                    'UNIT_TEST_ARGS=--collect-only tests/example',
                ),
                (
                    '-m popo check-python-policy',
                    'ruff format --check example.py',
                    'pytest --collect-only tests/example',
                ),
                id='quality',
            ),
        ],
    )
    def test_commands_are_overridable(
        self,
        make: MakeRunner,
        arguments: tuple[str, ...],
        expected_output: tuple[str, ...],
    ) -> None:
        result = make('--dry-run', *arguments)

        assert result.returncode == 0, result.stderr
        assert all(fragment in result.stdout for fragment in expected_output)

    def test_release_changelog_uses_project_python(
        self,
        make: MakeRunner,
    ) -> None:
        result = make(
            '--dry-run',
            'release-changelog',
            'RELEASE_VERSION=0.3.23',
            'PY=bootstrap-python',
            'PYTHON=project-python',
        )

        assert result.returncode == 0, result.stderr
        assert (
            'project-python -m popo check-release-changelog "0.3.23"' in result.stdout
        )
        assert 'bootstrap-python -m popo' not in result.stdout


# !SECTION
