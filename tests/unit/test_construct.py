"""CDK assertion tests for the reusable static-site construct."""

from collections.abc import Callable
from pathlib import Path

import aws_cdk as cdk
import pytest
from aws_cdk import assertions
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53

from aws_cdk_static_site import StaticSite, StaticSiteProps

type TemplateFactory = Callable[..., assertions.Template]

# SECTION: CONSTANTS


ACCOUNT = '111111111111'
CERTIFICATE_ARN = (
    f"arn:aws:acm:us-east-1:{ACCOUNT}:certificate/00000000-0000-0000-0000-000000000000"
)
SITE_PATH = Path(__file__).parents[2] / 'examples' / 'basic' / 'site'


# !SECTION


# SECTION: FIXTURES


@pytest.fixture(name='template_factory', scope='module')
def template_factory_fixture() -> TemplateFactory:
    """Return a factory that synthesizes a construct in a test stack."""

    def factory(
        *,
        deploy_content: bool = False,
        route53_enabled: bool = False,
        access_logs_enabled: bool = False,
    ) -> assertions.Template:
        app = cdk.App()
        stack = cdk.Stack(
            app,
            'TestStack',
            env=cdk.Environment(account=ACCOUNT, region='us-east-1'),
        )
        domain_names: tuple[str, ...] = ()
        certificate = None
        hosted_zone = None
        if route53_enabled:
            domain_names = ('example.com', 'www.example.com')
            hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
                stack,
                'HostedZone',
                hosted_zone_id='Z0000000000000000000',
                zone_name='example.com',
            )
        elif deploy_content:
            domain_names = ('www.example.com',)
            certificate = acm.Certificate.from_certificate_arn(
                stack,
                'Certificate',
                CERTIFICATE_ARN,
            )

        StaticSite(
            stack,
            'Site',
            props=StaticSiteProps(
                site_content_path=SITE_PATH if deploy_content else None,
                domain_names=domain_names,
                certificate=certificate,
                hosted_zone=hosted_zone,
                create_certificate=route53_enabled,
                create_route53_records=route53_enabled,
                enable_access_logs=access_logs_enabled,
            ),
        )
        return assertions.Template.from_stack(stack)

    return factory


# !SECTION


# SECTION: TESTS


class TestDelivery:
    """Verify CloudFront and deployment behavior."""

    def test_deploys_optional_content_with_cache_metadata(
        self,
        template_factory: TemplateFactory,
    ) -> None:
        template = template_factory(deploy_content=True)
        template.has_resource_properties(
            'Custom::CDKBucketDeployment',
            {
                'DistributionPaths': ['/*'],
                'Prune': True,
                'SystemMetadata': {
                    'cache-control': 'public, max-age=300, must-revalidate',
                },
            },
        )

    def test_rejects_missing_content_directory(self) -> None:
        app = cdk.App()
        stack = cdk.Stack(app, 'TestStack')

        with pytest.raises(ValueError, match='must identify a directory'):
            StaticSite(
                stack,
                'Site',
                props=StaticSiteProps(site_content_path='does-not-exist'),
            )

    def test_uses_oac_security_headers_and_cost_conscious_defaults(
        self,
        template_factory: TemplateFactory,
    ) -> None:
        template = template_factory()
        template.resource_count_is('AWS::CloudFront::OriginAccessControl', 1)
        template.has_resource_properties(
            'AWS::CloudFront::Distribution',
            {
                'DistributionConfig': assertions.Match.object_like(
                    {
                        'DefaultRootObject': 'index.html',
                        'HttpVersion': 'http2and3',
                        'PriceClass': 'PriceClass_100',
                    },
                ),
            },
        )
        template.has_resource_properties(
            'AWS::CloudFront::ResponseHeadersPolicy',
            {
                'ResponseHeadersPolicyConfig': assertions.Match.object_like(
                    {
                        'SecurityHeadersConfig': assertions.Match.object_like(
                            {'ContentSecurityPolicy': assertions.Match.any_value()},
                        ),
                    },
                ),
            },
        )


class TestOptionalIntegrations:
    """Verify DNS, certificate, and logging remain opt-in."""

    def test_creates_bounded_access_log_storage_when_requested(
        self,
        template_factory: TemplateFactory,
    ) -> None:
        template = template_factory(access_logs_enabled=True)
        template.resource_count_is('AWS::S3::Bucket', 2)
        template.has_resource_properties(
            'AWS::S3::Bucket',
            {
                'LifecycleConfiguration': {
                    'Rules': assertions.Match.array_with(
                        [
                            assertions.Match.object_like(
                                {'ExpirationInDays': 30},
                            ),
                        ],
                    ),
                },
            },
        )

    def test_creates_route53_aliases_and_certificate_when_requested(
        self,
        template_factory: TemplateFactory,
    ) -> None:
        template = template_factory(route53_enabled=True)
        template.resource_count_is('AWS::Route53::RecordSet', 4)
        template.has_resource_properties(
            'AWS::CertificateManager::Certificate',
            {
                'DomainName': 'example.com',
                'SubjectAlternativeNames': ['www.example.com'],
                'ValidationMethod': 'DNS',
            },
        )

    @pytest.mark.parametrize(
        ('environment', 'message'),
        [
            (
                cdk.Environment(account=ACCOUNT, region='us-west-2'),
                'requires stack region us-east-1; received us-west-2',
            ),
            (
                None,
                'requires an explicit stack region of us-east-1',
            ),
        ],
        ids=('incompatible-region', 'environment-agnostic'),
    )
    def test_rejects_invalid_region_for_created_certificate(
        self,
        environment: cdk.Environment | None,
        message: str,
    ) -> None:
        app = cdk.App()
        stack = cdk.Stack(app, 'TestStack', env=environment)
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            stack,
            'HostedZone',
            hosted_zone_id='Z0000000000000000000',
            zone_name='example.com',
        )

        with pytest.raises(ValueError, match=message):
            StaticSite(
                stack,
                'Site',
                props=StaticSiteProps(
                    domain_names=('www.example.com',),
                    hosted_zone=hosted_zone,
                    create_certificate=True,
                ),
            )


class TestStorage:
    """Verify the private origin's durability and security controls."""

    def test_creates_private_encrypted_versioned_bucket(
        self,
        template_factory: TemplateFactory,
    ) -> None:
        template = template_factory()
        template.has_resource_properties(
            'AWS::S3::Bucket',
            {
                'BucketEncryption': {
                    'ServerSideEncryptionConfiguration': [
                        {
                            'ServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256',
                            },
                        },
                    ],
                },
                'PublicAccessBlockConfiguration': {
                    'BlockPublicAcls': True,
                    'BlockPublicPolicy': True,
                    'IgnorePublicAcls': True,
                    'RestrictPublicBuckets': True,
                },
                'VersioningConfiguration': {'Status': 'Enabled'},
            },
        )
