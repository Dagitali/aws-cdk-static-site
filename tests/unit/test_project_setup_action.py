"""
:mod:`tests.unit.test_project_setup_action` module.

Contract tests for the shared GitHub Actions Python-project setup action.
"""

from pathlib import Path

# SECTION: CONSTANTS


ACTION_PATH = (
    Path(__file__).resolve().parents[2]
    / '.github'
    / 'actions'
    / 'setup-python-project'
    / 'action.yml'
)


# !SECTION


# SECTION: TESTS


class TestProjectSetupAction:
    """Verify the action's reusable input and execution contracts."""

    def test_installs_and_checks_dependencies_before_reporting(self) -> None:
        action = ACTION_PATH.read_text(encoding='utf-8')

        setup = action.index('- name: Set up Python')
        install = action.index('- name: Install project')
        report = action.index('- name: Report Python environment')

        assert setup < install < report
        assert "if: inputs.install == 'true'" in action
        assert 'python -m pip install "${install_args[@]}" "$target"' in action
        assert 'python -m pip check' in action

    def test_validates_boolean_inputs_before_environment_setup(self) -> None:
        action = ACTION_PATH.read_text(encoding='utf-8')

        validation = action.index('- name: Validate inputs')
        setup = action.index('- name: Set up Python')

        assert validation < setup
        assert action.count("default: 'true'") == 2
        assert action.count("must be 'true' or 'false'") == 2
        assert 'EDITABLE_INSTALL: ${{ inputs.editable }}' in action
        assert 'INSTALL_PROJECT: ${{ inputs.install }}' in action


# !SECTION
