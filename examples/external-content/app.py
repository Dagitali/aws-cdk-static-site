"""Provision delivery resources without creating a BucketDeployment."""

import aws_cdk as cdk

from aws_cdk_static_site import StaticSite

app = cdk.App()
stack = cdk.Stack(app, 'ExternalContentExample')
site = StaticSite(stack, 'Site')
cdk.CfnOutput(stack, 'ContentBucketName', value=site.bucket.bucket_name)
cdk.CfnOutput(
    stack,
    'DistributionId',
    value=site.distribution.distribution_id,
)
app.synth()
