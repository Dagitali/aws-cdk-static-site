# 0001: Use a Private S3 Origin with CloudFront OAC

Status: Accepted

- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)
- [Alternatives Considered](#alternatives-considered)
- [References](#references)

## Context

The construct needs to serve static content through CloudFront without making the S3 bucket a public
website endpoint. Consumers also need a composition that can be synthesized and tested without AWS
credentials.

## Decision

Create a public CloudFront distribution in front of a private, public-access-blocked S3 bucket and
authorize origin reads through CloudFront Origin Access Control. Redirect viewers to HTTPS and keep
S3 website hosting disabled.

## Consequences

The bucket cannot be used as a direct public website endpoint. Origin authorization is represented
in synthesized CloudFormation and can be regression-tested. Consumers receive CloudFront behavior,
pricing, propagation, and certificate constraints, including the `us-east-1` requirement for custom
domain certificates.

## Alternatives Considered

A public S3 website endpoint weakens the origin boundary and does not support the selected private
delivery model. Origin Access Identity is an older CloudFront mechanism; OAC is the repository's
implemented and tested model.

## References

- [`StaticSite` implementation](../../src/aws_cdk_static_site/construct.py)
- [Architecture](../../ARCHITECTURE.md)
- [Configuration reference](../CONFIGURATION.md)
