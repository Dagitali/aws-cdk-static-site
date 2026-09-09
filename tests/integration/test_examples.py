"""
:mod:`tests.integration.test_examples` module.

Integration tests that execute every documented example application and
verify independent CDK synthesis.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# SECTION: CONSTANTS


REPOSITORY_ROOT = Path(__file__).parents[2]
EXAMPLE_APPLICATIONS = tuple(
    sorted((REPOSITORY_ROOT / 'examples').glob('*/app.py')),
)


# !SECTION


# SECTION: TESTS


@pytest.mark.integration
class TestExampleApplications:
    """
    Verify every documented CDK application synthesizes independently.

    Each example runs in a subprocess with an isolated CDK output directory.
    """

    @pytest.mark.parametrize(
        'application',
        EXAMPLE_APPLICATIONS,
        ids=lambda path: path.parent.name,
    )
    def test_synthesizes(
        self,
        application: Path,
        tmp_path: Path,
    ) -> None:
        python_path = os.pathsep.join(
            filter(
                None,
                (str(REPOSITORY_ROOT / 'src'), os.environ.get('PYTHONPATH')),
            ),
        )
        environment = os.environ | {
            'CDK_OUTDIR': str(tmp_path / application.parent.name),
            'PYTHONPATH': python_path,
        }

        result = subprocess.run(
            [sys.executable, str(application)],
            cwd=REPOSITORY_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr


# !SECTION
