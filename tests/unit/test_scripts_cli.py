"""
:mod:`tests.unit.test_scripts_cli` module.

Unit tests for repository-maintenance command dispatch and reporting.
"""

from pathlib import Path

from scripts.__main__ import main

# SECTION: TESTS


class TestMain:
    """Verify successful and failing subcommand execution."""

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
