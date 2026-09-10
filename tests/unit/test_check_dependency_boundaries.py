"""
:mod:`tests.unit.test_check_dependency_boundaries` module.

Unit tests for runtime dependency lower-bound policy validation.
"""

from pathlib import Path

import pytest

from scripts.check_dependency_boundaries import validate

# SECTION: FIXTURES


@pytest.fixture(name='repository')
def repository_fixture(tmp_path: Path) -> Path:
    """
    Create matching dependency metadata and lowest constraints.

    Parameters
    ----------
    tmp_path : pathlib.Path
        Isolated test directory.

    Returns
    -------
    pathlib.Path
        Synthetic repository root.
    """
    (tmp_path / 'requirements').mkdir()
    (tmp_path / 'pyproject.toml').write_text(
        '[project]\n'
        'dependencies = [\n'
        '  "example-one>=1.2.3,<2.0.0",\n'
        '  "Example_Two>=4.5,<5",\n'
        ']\n',
        encoding='utf-8',
    )
    (tmp_path / 'requirements' / 'lowest.txt').write_text(
        'example-one==1.2.3\nexample-two==4.5\n',
        encoding='utf-8',
    )
    return tmp_path


# !SECTION


# SECTION: TESTS


class TestValidate:
    """
    Verify dependency-boundary metadata and constraint agreement.

    The suite covers matching definitions, version drift, unsupported metadata,
    malformed constraints, and missing policy files.
    """

    def test_accepts_matching_lower_bounds(self, repository: Path) -> None:
        assert validate(repository) == []

    def test_rejects_duplicate_metadata_dependencies(
        self,
        repository: Path,
    ) -> None:
        (repository / 'pyproject.toml').write_text(
            '[project]\n'
            'dependencies = [\n'
            '  "example-one>=1.2.3,<2.0.0",\n'
            '  "Example_One>=1.2.3,<2.0.0",\n'
            ']\n',
            encoding='utf-8',
        )

        assert 'duplicate dependency' in validate(repository)[0]

    def test_rejects_malformed_or_duplicate_constraints(
        self,
        repository: Path,
    ) -> None:
        (repository / 'requirements' / 'lowest.txt').write_text(
            'example-one>=1.2.3\nexample-two==4.5\nexample_two==4.5\n',
            encoding='utf-8',
        )

        failures = validate(repository)

        assert any('expected name==version' in failure for failure in failures)
        assert any('duplicate constraint' in failure for failure in failures)

    @pytest.mark.parametrize('missing', ['pyproject.toml', 'requirements/lowest.txt'])
    def test_rejects_missing_policy_file(
        self,
        repository: Path,
        missing: str,
    ) -> None:
        (repository / missing).unlink()

        assert 'does not exist' in validate(repository)[0]

    def test_rejects_unsupported_metadata(self, repository: Path) -> None:
        (repository / 'pyproject.toml').write_text(
            '[project]\ndependencies = ["example-one~=1.2"]\n',
            encoding='utf-8',
        )

        assert 'lower and upper bound' in validate(repository)[0]

    def test_rejects_version_drift(self, repository: Path) -> None:
        (repository / 'requirements' / 'lowest.txt').write_text(
            'example-one==1.2.4\nexample-two==4.5\n',
            encoding='utf-8',
        )

        assert 'expected' in validate(repository)[0]


# !SECTION
