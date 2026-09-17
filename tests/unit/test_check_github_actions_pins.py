"""
:mod:`tests.unit.test_check_github_actions_pins` module.

Unit tests for immutable GitHub Actions reference validation.
"""

from pathlib import Path

import pytest

from scripts.check_github_actions_pins import validate

# SECTION: TESTS


class TestValidate:
    """
    Verify remote, local, and container action-reference handling.

    The suite accepts immutable remote references and non-remote actions while
    rejecting mutable or malformed remote references.
    """

    def test_checks_composite_actions_recursively(self, tmp_path: Path) -> None:
        automation_dir = tmp_path / '.github'
        action_dir = automation_dir / 'actions' / 'setup-python-project'
        action_dir.mkdir(parents=True)
        (action_dir / 'action.yml').write_text(
            'runs:\n  using: composite\n  steps:\n'
            '    - uses: actions/setup-python@v7\n',
            encoding='utf-8',
        )

        failures = validate(automation_dir)

        assert len(failures) == 1
        assert 'actions/setup-python@v7' in failures[0]

    @pytest.mark.parametrize(
        ('reference', 'expected_failure'),
        [
            ('actions/checkout@' + 'a' * 40, False),
            ('./.github/actions/local', False),
            ('docker://alpine:3.23', False),
            ('actions/checkout@v7', True),
            ('actions/checkout', True),
        ],
        ids=('commit', 'local', 'container', 'tag', 'missing-revision'),
    )
    def test_classifies_action_reference(
        self,
        tmp_path: Path,
        reference: str,
        *,
        expected_failure: bool,
    ) -> None:
        automation_dir = tmp_path / '.github'
        workflow_dir = automation_dir / 'workflows'
        workflow_dir.mkdir(parents=True)
        (workflow_dir / 'ci.yml').write_text(
            f'steps:\n  - uses: {reference}\n',
            encoding='utf-8',
        )

        assert bool(validate(automation_dir)) is expected_failure

    def test_rejects_missing_automation_directory(self, tmp_path: Path) -> None:
        automation_dir = tmp_path / 'missing'

        assert validate(automation_dir) == [
            f'automation directory does not exist: {automation_dir}',
        ]


# !SECTION
