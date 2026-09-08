# Release Policy and Versioning

- [Scope](#scope)
- [Versioning Model](#versioning-model)
- [Pre-1.0 Stability](#pre-10-stability)
- [Patch Releases](#patch-releases)
- [Minor Releases](#minor-releases)
- [Major Releases](#major-releases)
- [Deprecation Policy](#deprecation-policy)
- [Release Artifacts](#release-artifacts)
- [Release Notes](#release-notes)
- [Supported Releases](#supported-releases)

## Scope

This public policy describes versioning, compatibility, and expected release artifacts. It excludes
credentials, account recovery, emergency access, and other private operator procedures.

## Versioning Model

The project follows [Semantic Versioning][semver] for its documented public interface:

- `MAJOR` releases may contain intentional breaking changes;
- `MINOR` releases add backward-compatible capability after `v1.0.0`; and
- `PATCH` releases contain backward-compatible fixes and release-hygiene corrections.

Release tags use `vMAJOR.MINOR.PATCH`, are annotated, and point to the authoritative merged `main`
commit. Package versions are derived from Git metadata by `setuptools-scm`.

## Pre-1.0 Stability

While the package is in `v0.x`, a minor release may change documented APIs or synthesized behavior.
Patch releases should remain backward compatible. Breaking changes should be explicit in release
notes and include migration guidance when practical.

## Patch Releases

Patch releases are appropriate for backward-compatible bug fixes, packaging corrections,
documentation repairs, dependency updates, and workflow changes that preserve the documented public
contract. A patch must not intentionally change required inputs or synthesized infrastructure in a
breaking way.

## Minor Releases

Before `v1.0.0`, minor releases may refine the public API or synthesized behavior and must document
breaking changes. After `v1.0.0`, minor releases should add backward-compatible capabilities such as
new optional properties, supported configurations, or additive resource behavior.

## Major Releases

Major releases are appropriate for intentional breaking changes to documented public interfaces or
synthesized behavior. They should identify affected consumers and provide migration guidance.

## Deprecation Policy

Before `v1.0.0`, deprecation periods are best effort. After `v1.0.0`, a documented public interface
should normally remain available for at least one minor release after its deprecation notice. An
accelerated removal requires a security, correctness, legal, or ecosystem-compatibility reason.

Internal modules, generated CDK identifiers, and undocumented implementation details are excluded
from this policy.

## Release Artifacts

A public package release is expected to include:

- An annotated Git tag;
- A GitHub Release with reviewed notes;
- Validated source and wheel distributions;
- SHA-256 checksums; and
- A CycloneDX dependency SBOM.

The repository does not publish to PyPI yet. Until a reviewed trusted-publishing workflow and
protected environment exist, maintainers must not upload distributions manually.

## Release Notes

Release notes should summarize user-visible changes, fixes, deprecations, breaking changes,
compatibility effects, and required migration steps. Use
[.github/RELEASE-NOTES-TEMPLATE.md](.github/RELEASE-NOTES-TEMPLATE.md), reconcile it with
`CHANGELOG.md`, and avoid exposing private infrastructure or incident details.

## Supported Releases

Before `v1.0.0`, the latest release is the maintenance target. A stable-line support policy will be
defined before the first stable release. See [SUPPORT.md](SUPPORT.md) for the current boundary.

[semver]: https://semver.org/
