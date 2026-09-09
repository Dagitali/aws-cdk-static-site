"""Shared pytest configuration for repository test layers."""

from pathlib import Path

import pytest

# SECTION: CONSTANTS


TESTS_ROOT = Path(__file__).parent
TEST_LAYERS = frozenset({'unit', 'integration', 'e2e', 'meta'})
pytest_plugins = ('tests.support.artifacts',)


# !SECTION


# SECTION: PYTEST HOOKS


def pytest_addoption(
    parser: pytest.Parser,
) -> None:
    """Register options shared by artifact-oriented test layers."""
    parser.addoption(
        '--artifact-dir',
        type=Path,
        help='Use prebuilt distributions from this directory.',
    )


def pytest_collection_modifyitems(
    items: list[pytest.Item],
) -> None:
    """Apply each test directory's layer marker during collection."""
    for item in items:
        try:
            layer = item.path.relative_to(TESTS_ROOT).parts[0]
        except ValueError as error:
            raise pytest.UsageError(
                f'{item.path} is outside the tests directory',
            ) from error
        if layer not in TEST_LAYERS:
            raise pytest.UsageError(
                f'{item.path.relative_to(TESTS_ROOT)} is outside a test layer',
            )
        item.add_marker(getattr(pytest.mark, layer))


# !SECTION
