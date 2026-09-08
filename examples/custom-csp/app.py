"""Replace the default Content Security Policy with a site-specific policy."""

import aws_cdk as cdk

from aws_cdk_static_site import StaticSite, StaticSiteProps

CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "base-uri 'self'; "
    "connect-src 'self' https://api.example.com; "
    "font-src 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'; "
    "img-src 'self' data: https://images.example.com; "
    "object-src 'none'; "
    "script-src 'self'; "
    "style-src 'self'; "
    'upgrade-insecure-requests'
)

app = cdk.App()
stack = cdk.Stack(app, 'CustomContentSecurityPolicyExample')
StaticSite(
    stack,
    'Site',
    props=StaticSiteProps(
        site_content_path='examples/basic/site',
        content_security_policy=CONTENT_SECURITY_POLICY,
    ),
)
app.synth()
