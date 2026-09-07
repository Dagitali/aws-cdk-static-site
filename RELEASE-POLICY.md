# Release Policy and Versioning

- [Scope](#scope)
- [Versioning Model](#versioning-model)
- [Pre-1.0 Stability](#pre-10-stability)
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

## Release Artifacts

A public package release is expected to include:

- an annotated Git tag;
- a GitHub Release with reviewed notes; and
- validated source and wheel distributions.

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
