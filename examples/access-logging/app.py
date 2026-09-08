"""Retain CloudFront access logs for a bounded period."""

import aws_cdk as cdk

from aws_cdk_static_site import StaticSite, StaticSiteProps

app = cdk.App()
stack = cdk.Stack(app, 'AccessLoggingExample')
site = StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(
        site_content_path='examples/basic/site',
        enable_access_logs=True,
        access_log_retention_days=14,
    ),
)
cdk.CfnOutput(
    stack,
    'AccessLogBucketName',
    value=site.access_log_bucket.bucket_name,
)
app.synth()
