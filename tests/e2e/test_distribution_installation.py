"""End-to-end installation tests for built distributions."""

import os
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

# SECTION: CONSTANTS


SMOKE_TEST = """
from importlib.metadata import version
from importlib.resources import files

from aws_cdk import App, Stack
from aws_cdk_static_site import StaticSite

app = App()
stack = Stack(app, 'ArtifactSmokeTest')
StaticSite(stack, 'Site')
app.synth()
assert files('aws_cdk_static_site').joinpath('py.typed').is_file()
assert version('aws-cdk-static-site')
"""


# !SECTION


# SECTION: TESTS


class TestDistributionInstallation:
    """Verify each published distribution installs and synthesizes in isolation."""

    @pytest.mark.parametrize(
        'artifact_fixture',
        ['wheel_path', 'sdist_path'],
        ids=['wheel', 'sdist'],
    )
    def test_installs_imports_and_synthesizes(
        self,
        artifact_fixture: str,
        request: pytest.FixtureRequest,
        tmp_path: Path,
    ) -> None:
        artifact = cast('Path', request.getfixturevalue(artifact_fixture))
        environment_path = tmp_path / artifact_fixture
        subprocess.run(
            [sys.executable, '-m', 'venv', str(environment_path)],
            check=True,
            timeout=60,
        )
        python = environment_path / (
            'Scripts/python.exe' if os.name == 'nt' else 'bin/python'
        )
        environment = os.environ.copy()
        environment.pop('PYTHONPATH', None)
        environment['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'

        subprocess.run(
            [str(python), '-m', 'pip', 'install', str(artifact)],
            cwd=tmp_path,
            env=environment,
            check=True,
            timeout=300,
        )
        subprocess.run(
            [str(python), '-c', SMOKE_TEST],
            cwd=tmp_path,
            env=environment,
            check=True,
            timeout=120,
        )


# !SECTION
