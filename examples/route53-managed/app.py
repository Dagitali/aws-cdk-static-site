"""Create CloudFront aliases and a DNS-validated certificate in Route 53."""

import aws_cdk as cdk
from aws_cdk import aws_route53 as route53

from aws_cdk_static_site import StaticSite, StaticSiteProps

app = cdk.App()
stack = cdk.Stack(
    app,
    'Route53ManagedExample',
    env=cdk.Environment(account='111111111111', region='us-east-1'),
)
hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
    stack,
    'HostedZone',
    hosted_zone_id='Z0000000000000000000',
    zone_name='example.com',
)
StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(
        site_content_path='examples/basic/site',
        domain_names=('example.com', 'www.example.com'),
        hosted_zone=hosted_zone,
        create_certificate=True,
        create_route53_records=True,
    ),
)
app.synth()
