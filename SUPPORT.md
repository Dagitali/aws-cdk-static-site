# Support

- [Support Policy](#support-policy)
- [Supported Versions](#supported-versions)
- [Supported Surface](#supported-surface)
- [Maintenance Expectations](#maintenance-expectations)
- [Where to Get Help](#where-to-get-help)
- [Response Targets](#response-targets)
- [Deprecation Policy](#deprecation-policy)

## Support Policy

This project is maintained as open source software with best-effort community support. Before
`v1.0.0`, its public API may change between minor releases as the package is validated in additional
consuming applications.

## Supported Versions

Before `v1.0.0`, the latest released version is the maintenance target. Older releases may continue
to work but should not be assumed to receive routine fixes or compatibility updates.

## Supported Surface

The support boundary includes the latest release, Python versions declared in `pyproject.toml`, and
the documented public API exported through the package root. Examples, internal modules, generated
identifiers, and behavior explicitly marked experimental are not compatibility promises.

For this package, the support boundary also includes documented synthesized infrastructure
behavior. Generated CDK logical IDs remain implementation details unless explicitly documented as a
contract.

AWS service behavior, quotas, pricing, and end-of-support policies remain governed by AWS. Consumers
are responsible for reviewing synthesized templates and deployed resources for their own security,
compliance, availability, and cost requirements.

## Maintenance Expectations

Before `v1.0.0`, minor releases are the normal vehicle for additive capabilities and deliberate API
refinement. Patch releases are reserved for targeted, backward-compatible maintenance such as:

- Confirmed regressions in documented behavior;
- Security fixes;
- Packaging, build, or installation failures; and
- Documentation or metadata corrections needed to keep a release usable.

Backports are not guaranteed. See [RELEASE-POLICY.md](RELEASE-POLICY.md) for versioning and
deprecation details.

## Where to Get Help

- Read the [README](README.md) and [documentation index](docs/README.md) first.
- Use a [GitHub issue][issues] for a reproducible bug or a concrete feature request.
- Follow [SECURITY.md](SECURITY.md) for suspected vulnerabilities.

Do not include AWS credentials, account identifiers, private domain data, or sensitive synthesized
templates in public reports.

## Response Targets

Maintainers target an initial response to complete security reports within three business days and
to ordinary issues within ten business days when capacity permits. These are goals, not guaranteed
service-level agreements.

## Deprecation Policy

Before `v1.0.0`, breaking changes may occur in minor releases and should be documented in release
notes and `CHANGELOG.md`. After `v1.0.0`, documented public interfaces should normally receive a
deprecation notice and migration path before removal unless security or correctness requires a
faster change.

[issues]: https://github.com/Dagitali/aws-cdk-static-site/issues
