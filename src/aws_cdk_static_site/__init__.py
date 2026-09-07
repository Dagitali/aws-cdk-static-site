"""Secure, cost-conscious static-site infrastructure for AWS CDK."""

from .construct import StaticSite
from .props import DEFAULT_CONTENT_SECURITY_POLICY, StaticSiteProps

# SECTION: PUBLIC API


__all__ = [
    'DEFAULT_CONTENT_SECURITY_POLICY',
    'StaticSite',
    'StaticSiteProps',
]


# !SECTION
