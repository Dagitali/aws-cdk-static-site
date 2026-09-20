"""
:mod:`tests.unit.test_script_support` module.

Unit tests for shared repository-maintenance helpers.
"""

from pathlib import Path

import pytest

from scripts._support import automation_paths, normalize_release, report

# SECTION: TESTS


class TestAutomationPaths:
    """Verify deterministic automation-file discovery."""

    def test_discovers_sorted_yaml_files(self, tmp_path: Path) -> None:
        nested = tmp_path / 'nested'
        nested.mkdir()
        expected = [tmp_path / 'a.yml', nested / 'b.yaml']
        for path in (*expected, tmp_path / 'ignored.json'):
            path.write_text('{}\n', encoding='utf-8')

        assert automation_paths(tmp_path) == expected


class TestNormalizeRelease:
    """Verify semantic release normalization."""

    @pytest.mark.parametrize('release', ['1.2.3', 'v1.2.3'])
    def test_accepts_supported_release_forms(self, release: str) -> None:
        assert normalize_release(release) == '1.2.3'

    def test_rejects_invalid_release(self) -> None:
        with pytest.raises(ValueError, match='vMAJOR.MINOR.PATCH'):
            normalize_release('release/1.2.3')


class TestReport:
    """Verify maintenance-command status and output reporting."""

    @pytest.mark.parametrize(
        ('failures', 'success', 'status', 'output'),
        [
            pytest.param(
                ['first', 'second'],
                'unused',
                1,
                'FAIL: first\nFAIL: second\n',
                id='failure',
            ),
            pytest.param(
                [],
                'validation passed',
                0,
                'PASS: validation passed\n',
                id='success',
            ),
        ],
    )
    def test_reports_results(
        self,
        capsys: pytest.CaptureFixture[str],
        failures: list[str],
        success: str,
        status: int,
        output: str,
    ) -> None:
        assert report(failures, success=success) == status
        assert capsys.readouterr().out == output


# !SECTION
