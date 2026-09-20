"""
:mod:`tests.unit.test_makefile` module.

Contract tests for repository-maintenance Make targets and safety boundaries.
"""

import subprocess
from pathlib import Path

import pytest

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
        repository_root: Path,
        tmp_path: Path,
        variable: str,
        safe_overrides: tuple[str, ...],
    ) -> None:
        result = subprocess.run(
            ('make', 'clean', *safe_overrides, f'{variable}={tmp_path}'),
            cwd=repository_root,
            capture_output=True,
            check=False,
            text=True,
        )

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
                    'ruff format --check example.py',
                    'pytest --collect-only tests/example',
                ),
                id='quality',
            ),
        ],
    )
    def test_commands_are_overridable(
        self,
        repository_root: Path,
        arguments: tuple[str, ...],
        expected_output: tuple[str, ...],
    ) -> None:
        result = subprocess.run(
            ('make', '--dry-run', *arguments),
            cwd=repository_root,
            capture_output=True,
            check=True,
            text=True,
        )

        assert all(fragment in result.stdout for fragment in expected_output)


# !SECTION
