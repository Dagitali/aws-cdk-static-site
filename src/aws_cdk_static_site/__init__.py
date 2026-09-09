"""
:mod:`aws_cdk_static_site` package.

Public facade for secure, cost-conscious static-site infrastructure built with
AWS CDK.

The package exports the :class:`StaticSite` construct, its
:class:`StaticSiteProps` configuration object, and the default Content Security
Policy.
"""

from .construct import StaticSite
from .props import DEFAULT_CONTENT_SECURITY_POLICY, StaticSiteProps

# SECTION: PUBLIC API


__all__ = [
    'DEFAULT_CONTENT_SECURITY_POLICY',
    'StaticSite',
    'StaticSiteProps',
]


# !SECTION
