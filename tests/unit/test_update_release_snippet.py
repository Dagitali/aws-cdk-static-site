"""Unit tests for the release installation-snippet updater."""

from pathlib import Path

import pytest

from scripts.update_release_snippet import END_MARKER, START_MARKER, render, update

# SECTION: FIXTURES


@pytest.fixture(name='readme')
def readme_fixture(
    tmp_path: Path,
) -> Path:
    """Create a README with a stale marked installation block."""
    readme = tmp_path / 'README.md'
    readme.write_text(
        f'Before\n{START_MARKER}\nstale\n{END_MARKER}\nAfter\n',
        encoding='utf-8',
    )
    return readme


# !SECTION


# SECTION: TESTS


class TestRender:
    """Verify deterministic release-snippet rendering."""

    @pytest.mark.parametrize('release', ['0.3.3', 'v0.3.3'])
    def test_normalizes_release_tag(
        self,
        release: str,
    ) -> None:
        assert '@v0.3.3"' in render(release)

    def test_rejects_invalid_release(self) -> None:
        with pytest.raises(ValueError, match='vMAJOR.MINOR.PATCH'):
            render('release/0.3.3')


class TestUpdate:
    """Verify update and check modes."""

    def test_updates_only_marked_content(
        self,
        readme: Path,
    ) -> None:
        assert update(readme, '0.3.3') == []

        content = readme.read_text(encoding='utf-8')
        assert content.startswith('Before\n')
        assert '@v0.3.3"' in content
        assert content.endswith('\nAfter\n')

    def test_accepts_current_snippet_in_check_mode(
        self,
        readme: Path,
    ) -> None:
        update(readme, '0.3.3')

        assert update(readme, 'v0.3.3', check=True) == []

    def test_rejects_stale_snippet_in_check_mode(
        self,
        readme: Path,
    ) -> None:
        assert update(readme, '0.3.3', check=True) == [
            'README.md installation snippet does not reference v0.3.3',
        ]

    def test_rejects_missing_markers(
        self,
        tmp_path: Path,
    ) -> None:
        readme = tmp_path / 'README.md'
        readme.write_text('No markers\n', encoding='utf-8')

        assert update(readme, '0.3.3') == [
            'README.md must contain one release installation marker pair',
        ]


# !SECTION
