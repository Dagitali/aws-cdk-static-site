"""
:mod:`tests.support.artifacts` module.

Session-scoped fixtures and helpers for locating or building distribution
artifacts used across test layers.
"""

import subprocess
import sys
from pathlib import Path

import pytest

# SECTION: CONSTANTS


REPOSITORY_ROOT = Path(__file__).parents[2]


# !SECTION


# SECTION: FIXTURES


@pytest.fixture(scope='session')
def distribution_directory(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """
    Return prebuilt artifacts or build them once for the test session.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Active request used to read the ``--artifact-dir`` option.
    tmp_path_factory : pytest.TempPathFactory
        Factory used to allocate an isolated build directory.

    Returns
    -------
    pathlib.Path
        Directory containing the source distribution and wheel.

    Raises
    ------
    pytest.fail.Exception
        If artifact construction fails or the selected directory is missing.
    """
    configured = request.config.getoption('--artifact-dir')
    if configured is not None:
        directory = Path(configured).expanduser().resolve()
    else:
        directory = tmp_path_factory.mktemp('distributions')
        result = subprocess.run(
            [
                sys.executable,
                '-m',
                'build',
                '--no-isolation',
                '--outdir',
                str(directory),
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode:
            pytest.fail(result.stdout + result.stderr, pytrace=False)

    if not directory.is_dir():
        pytest.fail(f'artifact directory does not exist: {directory}', pytrace=False)
    return directory


@pytest.fixture(scope='session')
def sdist_path(
    distribution_directory: Path,
) -> Path:
    """
    Return the session's single source-distribution artifact.

    Parameters
    ----------
    distribution_directory : pathlib.Path
        Directory containing built package artifacts.

    Returns
    -------
    pathlib.Path
        Sole ``.tar.gz`` source-distribution path.
    """
    return _single_artifact(distribution_directory, '*.tar.gz')


@pytest.fixture(scope='session')
def wheel_path(
    distribution_directory: Path,
) -> Path:
    """
    Return the session's single wheel artifact.

    Parameters
    ----------
    distribution_directory : pathlib.Path
        Directory containing built package artifacts.

    Returns
    -------
    pathlib.Path
        Sole wheel path.
    """
    return _single_artifact(distribution_directory, '*.whl')


# !SECTION


# SECTION: PROTECTED HELPERS


def _single_artifact(
    directory: Path,
    pattern: str,
) -> Path:
    """
    Return the sole artifact matching a glob pattern.

    Parameters
    ----------
    directory : pathlib.Path
        Directory containing built package artifacts.
    pattern : str
        Glob pattern selecting the desired artifact type.

    Returns
    -------
    pathlib.Path
        Sole matching artifact.

    Raises
    ------
    pytest.fail.Exception
        If the pattern does not match exactly one artifact.
    """
    artifacts = tuple(directory.glob(pattern))
    if len(artifacts) != 1:
        pytest.fail(
            f'expected one {pattern} artifact in {directory}; found {len(artifacts)}',
            pytrace=False,
        )
    return artifacts[0]


# !SECTION
