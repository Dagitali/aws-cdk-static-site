# Support

- [Support Policy](#support-policy)
- [Supported Surface](#supported-surface)
- [Where to Get Help](#where-to-get-help)
- [Response Expectations](#response-expectations)
- [Deprecation Policy](#deprecation-policy)

## Support Policy

AWS CDK Static Site is maintained as an open source project with best-effort community support.
Before `v1.0.0`, its public API may change between minor releases as the construct is validated in
additional consuming applications.

## Supported Surface

The support boundary includes the latest release, Python versions declared in `pyproject.toml`, and
the documented public API exported by `aws_cdk_static_site`. Examples, internal modules, generated
CDK logical IDs, and behavior explicitly marked experimental are not compatibility promises.

AWS service behavior, quotas, pricing, and end-of-support policies remain governed by AWS. Consumers
are responsible for reviewing synthesized templates and deployed resources for their own security,
compliance, availability, and cost requirements.

## Where to Get Help

- Read the [README](README.md) and [documentation index](docs/README.md) first.
- Use a [GitHub issue][issues] for a reproducible bug or a concrete feature request.
- Follow [SECURITY.md](SECURITY.md) for suspected vulnerabilities.

Do not include AWS credentials, account identifiers, private domain data, or sensitive synthesized
templates in public reports.

## Response Expectations

Maintainers target an initial response to complete security reports within three business days and
to ordinary issues within ten business days when capacity permits. These are goals, not guaranteed
service-level agreements.

## Deprecation Policy

Before `v1.0.0`, breaking changes may occur in minor releases and should be documented in release
notes and `CHANGELOG.md`. After `v1.0.0`, documented public interfaces should normally receive a
deprecation notice and migration path before removal unless security or correctness requires a
faster change.

[issues]: https://github.com/Dagitali/aws-cdk-static-site/issues
