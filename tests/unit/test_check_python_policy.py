"""
:mod:`tests.unit.test_check_python_policy` module.

Unit tests for resolving Python versions from GitHub Actions workflow syntax.
"""

import pytest

from scripts.check_python_policy import _resolve_workflow_versions

# SECTION: TESTS


class TestResolveWorkflowVersions:
    """
    Verify literal, environment, and matrix workflow version resolution.

    Unresolved expressions remain visible to the policy validator instead of
    being silently accepted.
    """

    def test_preserves_unresolved_expression(self) -> None:
        expression = '${{ matrix.python-version }}'

        assert _resolve_workflow_versions(expression, '') == (expression,)

    @pytest.mark.parametrize(
        ('value', 'content', 'expected'),
        [
            ('3.13', '', ('3.13',)),
            (
                '${{ env.DEFAULT_PYTHON_VERSION }}',
                'env:\n  DEFAULT_PYTHON_VERSION: "3.13"\n',
                ('3.13',),
            ),
            (
                '${{ matrix.python-version }}',
                'strategy:\n'
                '  matrix:\n'
                '    python-version:\n'
                '      - "3.13"\n'
                '      - "3.14"\n',
                ('3.13', '3.14'),
            ),
        ],
        ids=('literal', 'environment', 'matrix'),
    )
    def test_resolves_supported_workflow_forms(
        self,
        value: str,
        content: str,
        expected: tuple[str, ...],
    ) -> None:
        assert _resolve_workflow_versions(value, content) == expected


# !SECTION
