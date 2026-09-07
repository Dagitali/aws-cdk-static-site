"""Unit tests for static-site configuration validation."""

from typing import cast

import pytest
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53

from aws_cdk_static_site import StaticSiteProps

# SECTION: CONSTANTS


FAKE_CERTIFICATE = cast('acm.ICertificate', object())
FAKE_HOSTED_ZONE = cast('route53.IHostedZone', object())


# !SECTION


# SECTION: TESTS


class TestStaticSiteProps:
    """Verify invalid configuration combinations fail early."""

    def test_accepts_cloudfront_domain_without_custom_alias(self) -> None:
        assert StaticSiteProps().domain_names == ()

    @pytest.mark.parametrize(
        ('overrides', 'message'),
        [
            ({'default_root_object': ''}, 'must not be empty'),
            ({'error_document': ''}, 'must not be empty'),
            ({'domain_names': ('www.example.com',)}, 'certificate'),
            ({'create_certificate': True}, 'hosted_zone'),
            (
                {
                    'domain_names': ('www.example.com',),
                    'certificate': FAKE_CERTIFICATE,
                    'create_certificate': True,
                },
                'mutually exclusive',
            ),
            (
                {
                    'hosted_zone': FAKE_HOSTED_ZONE,
                    'create_certificate': True,
                },
                'domain_names',
            ),
            ({'create_route53_records': True}, 'hosted_zone'),
            (
                {
                    'hosted_zone': FAKE_HOSTED_ZONE,
                    'create_route53_records': True,
                },
                'domain_names',
            ),
            ({'access_log_retention_days': 0}, 'greater than zero'),
            ({'deployment_cache_max_age_seconds': -1}, 'must not be negative'),
            ({'content_security_policy': ''}, 'must not be empty'),
            (
                {
                    'domain_names': ('',),
                    'certificate': FAKE_CERTIFICATE,
                },
                'empty names',
            ),
            (
                {
                    'domain_names': ('example.com', 'example.com'),
                    'certificate': FAKE_CERTIFICATE,
                },
                'duplicates',
            ),
            ({'static_asset_paths': ('',)}, 'empty paths'),
            ({'static_asset_paths': ('assets/*', 'assets/*')}, 'duplicates'),
        ],
    )
    def test_rejects_invalid_configuration(
        self,
        overrides: dict[str, object],
        message: str,
    ) -> None:
        with pytest.raises(ValueError, match=message):
            StaticSiteProps(**overrides)  # type: ignore[arg-type]

# !SECTION
