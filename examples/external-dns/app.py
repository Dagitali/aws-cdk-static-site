"""Use an external DNS provider and an imported ACM certificate."""

import aws_cdk as cdk
from aws_cdk import aws_certificatemanager as acm

from aws_cdk_static_site import StaticSite, StaticSiteProps

app = cdk.App()
stack = cdk.Stack(
    app,
    'ExternalDnsExample',
    env=cdk.Environment(account='111111111111', region='us-east-1'),
)
certificate = acm.Certificate.from_certificate_arn(
    stack,
    'Certificate',
    'arn:aws:acm:us-east-1:111111111111:certificate/example',
)
site = StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(
        site_content_path='examples/basic/site',
        domain_names=('www.example.com',),
        certificate=certificate,
    ),
)
cdk.CfnOutput(
    stack,
    'ExternalDnsTarget',
    value=site.distribution.distribution_domain_name,
)
app.synth()
