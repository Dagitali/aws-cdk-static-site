"""
:mod:`aws_cdk_static_site.props` module.

Validated configuration for the reusable static-site construct.

The module defines conservative defaults for storage durability, CloudFront
delivery, browser security, cache metadata, and optional AWS integrations.
"""

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
    """
    Configure the resources created by :class:`~aws_cdk_static_site.StaticSite`.

    Parameters
    ----------
    site_content_path : str | pathlib.Path | None, optional
        Local directory deployed to the content bucket. Omit it when another
        process manages content.
    domain_names : tuple[str, ...], optional
        Custom hostnames served by CloudFront.
    certificate : aws_cdk.aws_certificatemanager.ICertificate | None, optional
        Existing ``us-east-1`` ACM certificate for *domain_names*.
    hosted_zone : aws_cdk.aws_route53.IHostedZone | None, optional
        Existing Route 53 zone used for certificate validation or aliases.
    create_certificate : bool, optional
        Create a DNS-validated ACM certificate in the consuming stack.
    create_route53_records : bool, optional
        Create IPv4 and IPv6 CloudFront aliases in *hosted_zone*.
    default_root_object : str, optional
        Object returned for requests to the distribution root.
    error_document : str, optional
        Object returned with the normalized 404 response.
    static_asset_paths : tuple[str, ...], optional
        CloudFront path patterns that use optimized asset caching.
    immutable_asset_paths : tuple[str, ...], optional
        Hashed-asset patterns deployed with long-lived immutable cache metadata.
    content_security_policy : str, optional
        Content Security Policy emitted through CloudFront response headers.
    price_class : aws_cdk.aws_cloudfront.PriceClass, optional
        CloudFront edge-location price class.
    enable_access_logs : bool, optional
        Store standard CloudFront access logs in a dedicated retained bucket.
    access_log_retention_days : int, optional
        Number of days to retain CloudFront access-log objects.
    bucket_removal_policy : aws_cdk.RemovalPolicy, optional
        CloudFormation removal policy for the content bucket.
    versioned : bool, optional
        Enable content-bucket object versioning.
    deployment_cache_max_age_seconds : int, optional
        Browser cache lifetime for revalidated content.
    immutable_asset_cache_max_age_seconds : int, optional
        Browser cache lifetime for immutable assets.

    Raises
    ------
    ValueError
        If required integrations are missing, mutually exclusive options are
        combined, cache or retention values are invalid, or configured names
        and paths are empty or duplicated.

    Notes
    -----
    Instances are immutable, slotted, and keyword-only. Validation runs before
    the construct creates AWS resources.
    """

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
    immutable_asset_paths: tuple[str, ...] = ()
    content_security_policy: str = DEFAULT_CONTENT_SECURITY_POLICY
    price_class: cloudfront.PriceClass = cloudfront.PriceClass.PRICE_CLASS_100
    enable_access_logs: bool = False
    access_log_retention_days: int = 30
    bucket_removal_policy: RemovalPolicy = RemovalPolicy.RETAIN
    versioned: bool = True
    deployment_cache_max_age_seconds: int = 300
    immutable_asset_cache_max_age_seconds: int = 31_536_000

    # !SECTION

    # SECTION: Magic Methods (Object Lifecycle)

    def __post_init__(self) -> None:
        """
        Reject incomplete or unsafe combinations before synthesis.

        Raises
        ------
        ValueError
            If an option violates a required configuration invariant.
        """
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
        if self.immutable_asset_cache_max_age_seconds <= 0:
            raise ValueError(
                'immutable_asset_cache_max_age_seconds must be greater than zero',
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
        if any(not path.strip() for path in self.immutable_asset_paths):
            raise ValueError('immutable_asset_paths must not contain empty paths')
        if len(set(self.immutable_asset_paths)) != len(self.immutable_asset_paths):
            raise ValueError('immutable_asset_paths must not contain duplicates')


# !SECTION
