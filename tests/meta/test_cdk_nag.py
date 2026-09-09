"""
:mod:`tests.meta.test_cdk_nag` module.

Meta tests that apply the reviewed ``cdk-nag`` AWS Solutions policy to
synthesized infrastructure.
"""

import aws_cdk as cdk
from aws_cdk import aws_certificatemanager as acm
from cdk_nag import AwsSolutionsChecks

from aws_cdk_static_site import StaticSite, StaticSiteProps
from tests.support.aws import TEST_ACCOUNT, TEST_CERTIFICATE_ARN

# SECTION: TESTS


class TestAwsSolutions:
    """
    Fail when ``cdk-nag`` reports an unreviewed AWS Solutions finding.

    Reviewed design-boundary suppressions remain explicit in the synthesized
    test stack so new findings cannot pass silently.
    """

    def test_has_no_unreviewed_findings(self) -> None:
        app = cdk.App()
        stack = cdk.Stack(
            app,
            'NagTest',
            env=cdk.Environment(account=TEST_ACCOUNT, region='us-east-1'),
        )
        certificate = acm.Certificate.from_certificate_arn(
            stack,
            'Certificate',
            TEST_CERTIFICATE_ARN,
        )
        StaticSite(
            stack,
            'Site',
            props=StaticSiteProps(
                domain_names=('www.example.com',),
                certificate=certificate,
                enable_access_logs=True,
            ),
        )
        cdk.Validations.of(app).add_plugins(AwsSolutionsChecks(app, verbose=True))
        cdk.Validations.of(stack).acknowledge(
            cdk.Acknowledgment(
                id='AwsSolutions-CFR1',
                reason='Geo restriction is a consumer-owned availability policy.',
            ),
            cdk.Acknowledgment(
                id='AwsSolutions-CFR2',
                reason='AWS WAF is an optional consumer-owned cost and risk decision.',
            ),
            cdk.Acknowledgment(
                id='AwsSolutions-S1',
                reason='S3 server access logging is outside this delivery construct.',
            ),
        )

        assembly = app.synth()

        assert assembly.get_stack_by_name(stack.stack_name)


# !SECTION
