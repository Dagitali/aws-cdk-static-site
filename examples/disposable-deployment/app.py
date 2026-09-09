#!/usr/bin/env python3
"""
Disposable deployment-test application.

Synthesize the tightly bounded AWS stack used by the manually approved
deployment test.

Notes
-----
The deployment workflow supplies the account, region, stack name, and output
directory through environment variables and destroys the stack after testing.
"""

import os

import aws_cdk as cdk

from aws_cdk_static_site import StaticSite, StaticSiteProps

# SECTION: CONFIGURATION


account = os.environ.get('CDK_DEFAULT_ACCOUNT', '111111111111')
region = os.environ.get('CDK_DEFAULT_REGION', 'us-east-1')
stack_name = os.environ.get(
    'DEPLOYMENT_TEST_STACK_NAME',
    'AwsCdkStaticSiteDisposableExample',
)


# !SECTION


# SECTION: APPLICATION


app = cdk.App(outdir=os.environ.get('CDK_OUTDIR', 'cdk.out'))
stack = cdk.Stack(
    app,
    stack_name,
    env=cdk.Environment(account=account, region=region),
    description='Disposable aws-cdk-static-site deployment test',
)
site = StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(
        bucket_removal_policy=cdk.RemovalPolicy.DESTROY,
        versioned=False,
    ),
)
cdk.Tags.of(stack).add('Purpose', 'DisposableDeploymentTest')
cdk.Tags.of(stack).add('GitHubRunId', os.environ.get('GITHUB_RUN_ID', 'local'))
cdk.CfnOutput(stack, 'DistributionDomainName', value=site.distribution.domain_name)
app.synth()


# !SECTION
