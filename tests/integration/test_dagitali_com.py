"""Integration tests using the dagitali.com consumer's real site content."""

import os
from pathlib import Path

import aws_cdk as cdk
import pytest
from aws_cdk import assertions
from aws_cdk import aws_certificatemanager as acm

from aws_cdk_static_site import StaticSite, StaticSiteProps
from tests.support.aws import TEST_ACCOUNT, TEST_CERTIFICATE_ARN

# SECTION: CONSTANTS


REPOSITORY_ROOT = Path(__file__).parents[2]


# !SECTION


# SECTION: FIXTURES


@pytest.fixture(name='dagitali_site_path', scope='module')
def dagitali_site_path_fixture() -> Path:
    """Locate an adjacent or explicitly checked-out dagitali.com site."""
    consumer_root = Path(
        os.environ.get(
            'DAGITALI_COM_PATH',
            REPOSITORY_ROOT.parent / 'dagitali.com',
        ),
    ).expanduser().resolve()
    site_path = consumer_root / 'site'
    if not (site_path / 'index.html').is_file():
        pytest.skip(f'dagitali.com site content not found under {consumer_root}')
    return site_path


# !SECTION


# SECTION: TESTS


class TestDagitaliComConsumer:
    """Verify the construct can represent dagitali.com's delivery layer."""

    def test_synthesizes_external_dns_site_content(
        self,
        dagitali_site_path: Path,
    ) -> None:
        app = cdk.App()
        stack = cdk.Stack(
            app,
            'DagitaliConsumerContract',
            env=cdk.Environment(account=TEST_ACCOUNT, region='us-east-1'),
        )
        certificate = acm.Certificate.from_certificate_arn(
            stack,
            'Certificate',
            TEST_CERTIFICATE_ARN,
        )
        StaticSite(
            stack,
            'Site',
            props=StaticSiteProps(
                site_content_path=dagitali_site_path,
                domain_names=('www.dagitali.com',),
                certificate=certificate,
                immutable_asset_paths=('assets/*.webp',),
            ),
        )
        template = assertions.Template.from_stack(stack)

        template.resource_count_is('AWS::CloudFront::OriginAccessControl', 1)
        template.resource_count_is('Custom::CDKBucketDeployment', 2)
        template.has_resource_properties(
            'AWS::CloudFront::Distribution',
            {
                'DistributionConfig': assertions.Match.object_like(
                    {'Aliases': ['www.dagitali.com']},
                ),
            },
        )


# !SECTION
