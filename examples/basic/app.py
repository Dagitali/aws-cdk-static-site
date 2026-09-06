"""Minimal CDK application using the reusable construct."""

import aws_cdk as cdk

from aws_cdk_static_site import StaticSite, StaticSiteProps

app = cdk.App()
stack = cdk.Stack(app, 'ExampleStaticSite')
StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(site_content_path='examples/basic/site'),
)
app.synth()
