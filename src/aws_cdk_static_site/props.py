"""Configuration for the reusable static-site construct."""

from dataclasses import dataclass
from pathlib import Path

from aws_cdk import RemovalPolicy
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_route53 as route53

# SECTION: CONSTANTS


DEFAULT_CONTENT_SECURITY_POLICY = (
    "default-src 'self'; base-uri 'self'; connect-src 'self'; "
    "font-src 'self'; form-action 'self'; frame-ancestors 'none'; "
    "img-src 'self' data:; object-src 'none'; script-src 'self'; "
    "style-src 'self'; upgrade-insecure-requests"
)


# !SECTION


# SECTION: DATA CLASSES


@dataclass(frozen=True, slots=True, kw_only=True)
class StaticSiteProps:
    """Configure the resources created by :class:`StaticSite`."""

    # SECTION: Attributes

    site_content_path: str | Path | None = None
    domain_names: tuple[str, ...] = ()
    certificate: acm.ICertificate | None = None
    hosted_zone: route53.IHostedZone | None = None
    create_certificate: bool = False
    create_route53_records: bool = False
    default_root_object: str = 'index.html'
    error_document: str = '404.html'
    static_asset_paths: tuple[str, ...] = (
        'assets/*',
        'favicon.ico',
        'og.png',
    )
    content_security_policy: str = DEFAULT_CONTENT_SECURITY_POLICY
    price_class: cloudfront.PriceClass = cloudfront.PriceClass.PRICE_CLASS_100
    enable_access_logs: bool = False
    access_log_retention_days: int = 30
    bucket_removal_policy: RemovalPolicy = RemovalPolicy.RETAIN
    versioned: bool = True
    deployment_cache_max_age_seconds: int = 300

    # !SECTION

    # SECTION: Magic Methods (Object Lifecycle)

    def __post_init__(self) -> None:
        """Reject incomplete or unsafe combinations before synthesis."""
        if not self.default_root_object.strip():
            raise ValueError('default_root_object must not be empty')
        if not self.error_document.strip():
            raise ValueError('error_document must not be empty')
        if self.domain_names and not (self.certificate or self.create_certificate):
            raise ValueError(
                'certificate or create_certificate is required with domain_names',
            )
        if self.certificate and self.create_certificate:
            raise ValueError(
                'certificate and create_certificate are mutually exclusive',
            )
        if self.create_certificate and not self.hosted_zone:
            raise ValueError('hosted_zone is required to create a certificate')
        if self.create_certificate and not self.domain_names:
            raise ValueError('domain_names is required to create a certificate')
        if self.create_route53_records and not self.hosted_zone:
            raise ValueError('hosted_zone is required to create Route 53 records')
        if self.create_route53_records and not self.domain_names:
            raise ValueError('domain_names is required to create Route 53 records')
        if self.access_log_retention_days <= 0:
            raise ValueError('access_log_retention_days must be greater than zero')
        if self.deployment_cache_max_age_seconds < 0:
            raise ValueError(
                'deployment_cache_max_age_seconds must not be negative',
            )
        if not self.content_security_policy.strip():
            raise ValueError('content_security_policy must not be empty')
        if any(not name.strip() for name in self.domain_names):
            raise ValueError('domain_names must not contain empty names')
        if len(set(self.domain_names)) != len(self.domain_names):
            raise ValueError('domain_names must not contain duplicates')
        if any(not path.strip() for path in self.static_asset_paths):
            raise ValueError('static_asset_paths must not contain empty paths')
        if len(set(self.static_asset_paths)) != len(self.static_asset_paths):
            raise ValueError('static_asset_paths must not contain duplicates')


# !SECTION
