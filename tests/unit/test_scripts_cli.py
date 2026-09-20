"""
:mod:`tests.unit.test_scripts_cli` module.

Unit tests for repository-maintenance command dispatch and reporting.
"""

from pathlib import Path

import pytest

from scripts.__main__ import main

# SECTION: TESTS


class TestMain:
    """Verify successful and failing subcommand execution."""

    def test_dispatches_documentation_check(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        tmp_path.joinpath('README.md').write_text(
            '[missing](missing.md)\n',
            encoding='utf-8',
        )

        assert main(['check-docs', '--root', str(tmp_path)]) == 1
        assert 'missing link target' in capsys.readouterr().out

    def test_dispatches_github_actions_pin_check_and_compatibility_alias(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        automation_dir = tmp_path / '.github' / 'workflows'
        automation_dir.mkdir(parents=True)
        (automation_dir / 'ci.yml').write_text(
            f'steps:\n  - uses: actions/checkout@{'a' * 40}\n',
            encoding='utf-8',
        )

        arguments = ['--automation-dir', str(tmp_path / '.github')]

        assert main(['check-github-actions-pins', *arguments]) == 0
        assert 'deprecated' not in capsys.readouterr().err

        assert main(['check-workflow-pins', *arguments]) == 0
        assert "'check-workflow-pins' is deprecated" in capsys.readouterr().err

    def test_dispatches_release_changelog_check(
        self,
        tmp_path: Path,
    ) -> None:
        changelog = tmp_path / 'CHANGELOG.md'
        changelog.write_text('## 1.2.3 - 2026-09-10\n', encoding='utf-8')

        result = main(
            [
                'check-release-changelog',
                'v1.2.3',
                '--changelog',
                str(changelog),
            ],
        )

        assert result == 0

    def test_reports_invalid_release(self, tmp_path: Path) -> None:
        result = main(
            [
                'check-release-changelog',
                '1.2',
                '--changelog',
                str(tmp_path / 'CHANGELOG.md'),
            ],
        )

        assert result == 1


# !SECTION
