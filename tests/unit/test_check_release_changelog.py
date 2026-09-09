"""Unit tests for the release-changelog policy checker."""

from pathlib import Path

import pytest

from scripts.check_release_changelog import validate

# SECTION: TESTS


class TestValidate:
    """Verify release-version and changelog-section validation."""

    @pytest.mark.parametrize('release', ['0.2.2', 'v0.2.2'])
    def test_accepts_dated_section(
        self,
        tmp_path: Path,
        release: str,
    ) -> None:
        changelog = tmp_path / 'CHANGELOG.md'
        changelog.write_text('## 0.2.2 - 2026-09-08\n', encoding='utf-8')

        assert validate(changelog, release) == []

    def test_rejects_invalid_calendar_date(
        self,
        tmp_path: Path,
    ) -> None:
        changelog = tmp_path / 'CHANGELOG.md'
        changelog.write_text('## 0.2.2 - 2026-02-30\n', encoding='utf-8')

        assert validate(changelog, '0.2.2') == [
            'CHANGELOG.md has an invalid date for 0.2.2: 2026-02-30',
        ]

    @pytest.mark.parametrize(
        ('release', 'expected'),
        [
            ('release/0.2.2', 'release version must use'),
            ('0.2', 'release version must use'),
            ('0.2.02', 'release version must use'),
        ],
    )
    def test_rejects_invalid_version(
        self,
        tmp_path: Path,
        release: str,
        expected: str,
    ) -> None:
        assert expected in validate(tmp_path / 'CHANGELOG.md', release)[0]

    def test_rejects_missing_changelog(
        self,
        tmp_path: Path,
    ) -> None:
        failures = validate(tmp_path / 'CHANGELOG.md', '0.2.2')

        assert failures == [f'changelog does not exist: {tmp_path / 'CHANGELOG.md'}']

    def test_rejects_missing_release_section(
        self,
        tmp_path: Path,
    ) -> None:
        changelog = tmp_path / 'CHANGELOG.md'
        changelog.write_text('## Unreleased\n', encoding='utf-8')

        assert validate(changelog, '0.2.2') == [
            'CHANGELOG.md has no dated section for 0.2.2',
        ]


# !SECTION
