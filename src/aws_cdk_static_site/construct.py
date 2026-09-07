"""Reusable AWS CDK construct for private static-site delivery."""

from pathlib import Path
from typing import cast

from aws_cdk import Duration, RemovalPolicy, Stack, Token
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct

from .props import StaticSiteProps

# SECTION: PROTECTED CONSTANTS


_CLOUDFRONT_CERTIFICATE_REGION = 'us-east-1'


# !SECTION

# SECTION: AWS CDK CONSTRUCTS


class StaticSite(Construct):
    """
    Provision secure storage, delivery, and optional DNS for a static site.
    """

    # SECTION: Magic Methods (Object Lifecycle)

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        props: StaticSiteProps | None = None,
    ) -> None:
        """Create the static-site resources."""
        super().__init__(scope, construct_id)
        props = props or StaticSiteProps()
        self._validate_certificate_region(props)

        self.bucket = self._create_content_bucket(props)
        self.access_log_bucket = self._create_access_log_bucket(props)
        self.response_headers_policy = self._create_response_headers_policy(props)
        self.certificate = self._resolve_certificate(props)
        self.distribution = self._create_distribution(props)
        self.dns_records = self._create_dns_records(props)
        self.deployment = self._create_deployment(props)

    # !SECTION

    # SECTION: Protected Instance Methods

    def _create_access_log_bucket(
        self,
        props: StaticSiteProps,
    ) -> s3.Bucket | None:
        if not props.enable_access_logs:
            return None
        return s3.Bucket(
            self,
            'AccessLogBucket',
            access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,
            removal_policy=RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(props.access_log_retention_days),
                ),
            ],
        )

    def _create_content_bucket(
        self,
        props: StaticSiteProps,
    ) -> s3.Bucket:
        return s3.Bucket(
            self,
            'ContentBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            versioned=props.versioned,
            removal_policy=props.bucket_removal_policy,
            auto_delete_objects=False,
            lifecycle_rules=[
                s3.LifecycleRule(
                    noncurrent_version_expiration=Duration.days(30),
                    abort_incomplete_multipart_upload_after=Duration.days(7),
                ),
            ],
        )

    def _create_response_headers_policy(
        self,
        props: StaticSiteProps,
    ) -> cloudfront.ResponseHeadersPolicy:
        return cloudfront.ResponseHeadersPolicy(
            self,
            'SecurityHeaders',
            security_headers_behavior=cloudfront.ResponseSecurityHeadersBehavior(
                content_security_policy=(
                    cloudfront.ResponseHeadersContentSecurityPolicy(
                        content_security_policy=props.content_security_policy,
                        override=True,
                    )
                ),
                content_type_options=cloudfront.ResponseHeadersContentTypeOptions(
                    override=True,
                ),
                frame_options=cloudfront.ResponseHeadersFrameOptions(
                    frame_option=cloudfront.HeadersFrameOption.DENY,
                    override=True,
                ),
                referrer_policy=cloudfront.ResponseHeadersReferrerPolicy(
                    referrer_policy=(
                        cloudfront.HeadersReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN
                    ),
                    override=True,
                ),
                strict_transport_security=(
                    cloudfront.ResponseHeadersStrictTransportSecurity(
                        access_control_max_age=Duration.days(730),
                        include_subdomains=True,
                        preload=True,
                        override=True,
                    )
                ),
                xss_protection=cloudfront.ResponseHeadersXSSProtection(
                    protection=True,
                    mode_block=True,
                    override=True,
                ),
            ),
            custom_headers_behavior=cloudfront.ResponseCustomHeadersBehavior(
                custom_headers=[
                    cloudfront.ResponseCustomHeader(
                        header='Permissions-Policy',
                        value=(
                            'camera=(), geolocation=(), microphone=(), '
                            'payment=(), usb=()'
                        ),
                        override=True,
                    ),
                    cloudfront.ResponseCustomHeader(
                        header='Cross-Origin-Opener-Policy',
                        value='same-origin',
                        override=True,
                    ),
                ],
            ),
        )

    def _resolve_certificate(
        self,
        props: StaticSiteProps,
    ) -> acm.ICertificate | None:
        if props.certificate:
            return props.certificate
        if not props.create_certificate:
            return None
        hosted_zone = cast('route53.IHostedZone', props.hosted_zone)
        return acm.Certificate(
            self,
            'Certificate',
            domain_name=props.domain_names[0],
            subject_alternative_names=list(props.domain_names[1:]),
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

    def _create_deployment(
        self,
        props: StaticSiteProps,
    ) -> s3deploy.BucketDeployment | None:
        if props.site_content_path is None:
            return None
        site_content_path = Path(props.site_content_path).expanduser().resolve()
        if not site_content_path.is_dir():
            raise ValueError(
                f"site_content_path must identify a directory: {site_content_path}",
            )

        log_group = logs.LogGroup(
            self,
            'DeploymentLogs',
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY,
        )
        deployment = s3deploy.BucketDeployment(
            self,
            'ContentDeployment',
            sources=[s3deploy.Source.asset(str(site_content_path))],
            destination_bucket=self.bucket,
            cache_control=[
                s3deploy.CacheControl.set_public(),
                s3deploy.CacheControl.max_age(
                    Duration.seconds(props.deployment_cache_max_age_seconds),
                ),
                s3deploy.CacheControl.must_revalidate(),
            ],
            distribution=self.distribution,
            distribution_paths=['/*'],
            prune=True,
            retain_on_delete=True,
            memory_limit=512,
            log_group=log_group,
        )
        deployment.node.add_dependency(self.distribution)
        return deployment

    def _create_distribution(
        self,
        props: StaticSiteProps,
    ) -> cloudfront.Distribution:
        origin = origins.S3BucketOrigin.with_origin_access_control(self.bucket)
        html_behavior = cloudfront.BehaviorOptions(
            origin=origin,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
            cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
            response_headers_policy=self.response_headers_policy,
            compress=True,
        )
        asset_behavior = cloudfront.BehaviorOptions(
            origin=origin,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
            cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            response_headers_policy=self.response_headers_policy,
            compress=True,
        )
        additional_behaviors = {
            '*.html': html_behavior,
            **{path: asset_behavior for path in props.static_asset_paths},
        }
        return cloudfront.Distribution(
            self,
            'Distribution',
            default_root_object=props.default_root_object,
            domain_names=list(props.domain_names),
            certificate=self.certificate,
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
            http_version=cloudfront.HttpVersion.HTTP2_AND_3,
            enable_ipv6=True,
            price_class=props.price_class,
            enable_logging=props.enable_access_logs,
            log_bucket=self.access_log_bucket,
            default_behavior=html_behavior,
            additional_behaviors=additional_behaviors,
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=status,
                    response_http_status=404,
                    response_page_path=f"/{props.error_document}",
                    ttl=Duration.minutes(5),
                )
                for status in (403, 404)
            ],
        )

    def _create_dns_records(
        self,
        props: StaticSiteProps,
    ) -> tuple[route53.ARecord | route53.AaaaRecord, ...]:
        if not props.create_route53_records:
            return ()
        hosted_zone = cast('route53.IHostedZone', props.hosted_zone)

        records: list[route53.ARecord | route53.AaaaRecord] = []
        for index, domain_name in enumerate(props.domain_names):
            target = route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution),
            )
            records.extend(
                (
                    route53.ARecord(
                        self,
                        f"AliasA{index}",
                        zone=hosted_zone,
                        record_name=domain_name,
                        target=target,
                    ),
                    route53.AaaaRecord(
                        self,
                        f"AliasAaaa{index}",
                        zone=hosted_zone,
                        record_name=domain_name,
                        target=target,
                    ),
                ),
            )
        return tuple(records)

    def _validate_certificate_region(self, props: StaticSiteProps) -> None:
        if not props.create_certificate:
            return

        region = Stack.of(self).region
        if Token.is_unresolved(region):
            raise ValueError(
                'create_certificate requires an explicit stack region of '
                f'{_CLOUDFRONT_CERTIFICATE_REGION}',
            )
        if region != _CLOUDFRONT_CERTIFICATE_REGION:
            raise ValueError(
                'create_certificate requires stack region '
                f'{_CLOUDFRONT_CERTIFICATE_REGION}; received {region}',
            )


# !SECTION
