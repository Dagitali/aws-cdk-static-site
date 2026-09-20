"""
:mod:`tests.unit.test_check_docs` module.

Unit tests for repository-local Markdown link validation.
"""

from pathlib import Path

import pytest

from scripts.check_docs import validate

# SECTION: TESTS


class TestValidate:
    """Verify repository-local Markdown links and anchors."""

    def test_accepts_a_relative_repository_root(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        tmp_path.joinpath('README.md').write_text(
            '[self](README.md)\n',
            encoding='utf-8',
        )
        monkeypatch.chdir(tmp_path)

        assert validate(Path('.')) == []

    def test_accepts_files_directories_and_heading_anchors(
        self,
        tmp_path: Path,
    ) -> None:
        docs = tmp_path / 'docs'
        docs.mkdir()
        docs.joinpath('guide.md').write_text(
            '# Set Up\n\n## Repeat\n\n## Repeat\n',
            encoding='utf-8',
        )
        tmp_path.joinpath('README.md').write_text(
            '[guide](docs/guide.md#set-up) '
            '[duplicate](docs/guide.md#repeat-1) '
            '[query](docs/guide.md?view=full#set-up) '
            '[external](HTTPS://example.com/missing.md) '
            '[docs](docs/)\n',
            encoding='utf-8',
        )

        assert validate(tmp_path) == []

    def test_ignores_mixed_fence_markers_and_hidden_directories(
        self,
        tmp_path: Path,
    ) -> None:
        tmp_path.joinpath('README.md').write_text(
            '```markdown\n~~~\n```python\n[example](missing.md)\n```\n',
            encoding='utf-8',
        )
        hidden = tmp_path / '.cache'
        hidden.mkdir()
        hidden.joinpath('README.md').write_text(
            '[generated](missing.md)\n',
            encoding='utf-8',
        )

        assert validate(tmp_path) == []

    def test_reports_missing_targets_anchors_and_repository_escapes(
        self,
        tmp_path: Path,
    ) -> None:
        tmp_path.joinpath('guide.md').write_text(
            '# Existing\n',
            encoding='utf-8',
        )
        tmp_path.joinpath('README.md').write_text(
            '[missing](missing.md) [anchor](guide.md#absent) [escape](../outside.md)\n',
            encoding='utf-8',
        )

        failures = validate(tmp_path)

        assert len(failures) == 3
        assert any('missing link target' in failure for failure in failures)
        assert any('missing anchor' in failure for failure in failures)
        assert any('link escapes repository' in failure for failure in failures)

    def test_validates_reference_style_links(self, tmp_path: Path) -> None:
        tmp_path.joinpath('README.md').write_text(
            '[guide]: docs/missing.md\n',
            encoding='utf-8',
        )

        assert validate(tmp_path) == [
            'README.md:1: missing link target: docs/missing.md',
        ]

    def test_rejects_missing_repository_root(self, tmp_path: Path) -> None:
        root = tmp_path / 'missing'

        assert validate(root) == [f'repository root does not exist: {root}']


# !SECTION
