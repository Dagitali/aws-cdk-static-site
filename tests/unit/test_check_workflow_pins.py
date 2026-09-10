"""
:mod:`tests.unit.test_check_workflow_pins` module.

Unit tests for immutable GitHub Actions reference validation.
"""

from pathlib import Path

import pytest

from scripts.check_workflow_pins import validate

# SECTION: TESTS


class TestValidate:
    """
    Verify remote, local, and container action-reference handling.

    The suite accepts immutable remote references and non-remote actions while
    rejecting mutable or malformed remote references.
    """

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
        workflow_dir = tmp_path / '.github' / 'workflows'
        workflow_dir.mkdir(parents=True)
        (workflow_dir / 'ci.yml').write_text(
            f'steps:\n  - uses: {reference}\n',
            encoding='utf-8',
        )

        assert bool(validate(workflow_dir)) is expected_failure

    def test_rejects_missing_workflow_directory(self, tmp_path: Path) -> None:
        workflow_dir = tmp_path / 'missing'

        assert validate(workflow_dir) == [
            f'workflow directory does not exist: {workflow_dir}',
        ]


# !SECTION
