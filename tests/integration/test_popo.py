"""
:mod:`tests.integration.test_popo` module.

Integration contracts for the external repository-policy CLI.
"""

import re
from pathlib import Path

import pytest
from popo.cli import main
from popo.config import load_config

# SECTION: TESTS


class TestPopoIntegration:
    """Verify Popo loads and enforces this repository's consumer policy."""

    def test_automation_uses_the_configured_revision(
        self,
        repository_root: Path,
    ) -> None:
        metadata = repository_root.joinpath('pyproject.toml').read_text(
            encoding='utf-8',
        )
        revision_match = re.search(
            r'popo\.git@(?P<revision>[0-9a-f]{40})',
            metadata,
        )
        assert revision_match is not None

        revision = revision_match.group('revision')
        ci = repository_root.joinpath('.github/workflows/ci.yml').read_text(
            encoding='utf-8',
        )
        cd = repository_root.joinpath('.github/workflows/cd.yml').read_text(
            encoding='utf-8',
        )

        assert 'python -m popo check-release-changelog' in ci
        assert f'POPO_REVISION: {revision}' in cd
        assert 'python -m popo check-release-changelog' in cd
        assert 'python -m scripts' not in ci + cd

    def test_loads_explicit_consumer_configuration(
        self,
        repository_root: Path,
    ) -> None:
        config = load_config(repository_root)

        assert config.dependencies.metadata == repository_root / 'pyproject.toml'
        assert config.dependencies.requirements == (
            repository_root / 'requirements' / 'lowest.txt'
        )
        assert config.dependencies.mode == 'minimum-constraints'
        assert config.python_policy.requires_python == '>=3.13,<3.15'
        assert config.python_policy.python_version == '3.13'

    @pytest.mark.parametrize(
        'command',
        [
            'check-dependency-boundaries',
            'check-github-actions-pins',
            'check-python-policy',
        ],
    )
    def test_repository_policy_passes(
        self,
        repository_root: Path,
        command: str,
    ) -> None:
        assert main([command, '--root', str(repository_root)]) == 0


# !SECTION
