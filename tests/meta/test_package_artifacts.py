"""Distribution-content and metadata contract tests."""

import tarfile
from email import policy
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

# SECTION: CONSTANTS


PACKAGE_PATH = 'aws_cdk_static_site'


# !SECTION


# SECTION: TESTS


class TestSourceDistributionContents:
    """Verify source releases remain buildable and legally complete."""

    def test_contains_build_typing_and_legal_files(
        self,
        sdist_path: Path,
    ) -> None:
        with tarfile.open(sdist_path, mode='r:gz') as archive:
            names = set(archive.getnames())

        expected_suffixes = {
            '/LICENSE',
            '/NOTICE',
            '/pyproject.toml',
            f'/src/{PACKAGE_PATH}/py.typed',
        }
        assert all(
            any(name.endswith(suffix) for name in names)
            for suffix in expected_suffixes
        )


class TestWheelContents:
    """Verify the wheel contains the public package and legal metadata."""

    def test_contains_license_and_notice(
        self,
        wheel_path: Path,
    ) -> None:
        with ZipFile(wheel_path) as archive:
            names = set(archive.namelist())

        assert any(name.endswith('.dist-info/licenses/LICENSE') for name in names)
        assert any(name.endswith('.dist-info/licenses/NOTICE') for name in names)

    def test_contains_runtime_and_typing_files(
        self,
        wheel_path: Path,
    ) -> None:
        with ZipFile(wheel_path) as archive:
            names = set(archive.namelist())

        assert {
            f'{PACKAGE_PATH}/__init__.py',
            f'{PACKAGE_PATH}/construct.py',
            f'{PACKAGE_PATH}/props.py',
            f'{PACKAGE_PATH}/py.typed',
        } <= names


class TestWheelMetadata:
    """Verify installed-package metadata reflects the public support contract."""

    def test_declares_identity_license_and_python_support(
        self,
        wheel_path: Path,
    ) -> None:
        with ZipFile(wheel_path) as archive:
            metadata_name = next(
                name
                for name in archive.namelist()
                if name.endswith('.dist-info/METADATA')
            )
            metadata = BytesParser(policy=policy.default).parsebytes(
                archive.read(metadata_name),
            )

        assert metadata['Name'] == 'aws-cdk-static-site'
        assert metadata['License-Expression'] == 'MIT'
        assert set(metadata['Requires-Python'].split(',')) == {'>=3.13', '<3.15'}
        assert {
            'Programming Language :: Python :: 3.13',
            'Programming Language :: Python :: 3.14',
            'Typing :: Typed',
        } <= set(metadata.get_all('Classifier') or [])
        requirements = metadata.get_all('Requires-Dist') or []
        assert any(
            requirement.startswith('aws-cdk-lib') for requirement in requirements
        )
        assert any(requirement.startswith('constructs') for requirement in requirements)


# !SECTION
