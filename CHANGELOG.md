# Changelog

All notable changes to this project will be documented in this file.

- [Unreleased](#unreleased)
- [0.3.0 - 2026-09-08](#030---2026-09-08)
- [0.2.9 - 2026-09-08](#029---2026-09-08)
- [0.2.8 - 2026-09-08](#028---2026-09-08)
- [0.2.7 - 2026-09-08](#027---2026-09-08)
- [0.2.6 - 2026-09-08](#026---2026-09-08)
- [0.2.5 - 2026-09-08](#025---2026-09-08)
- [0.2.4 - 2026-09-08](#024---2026-09-08)
- [0.2.3 - 2026-09-08](#023---2026-09-08)
- [0.2.2 - 2026-09-08](#022---2026-09-08)
- [0.2.1 - 2026-09-08](#021---2026-09-08)
- [0.2.0 - 2026-09-08](#020---2026-09-08)

## Unreleased

## 0.3.0 - 2026-09-08

- Add distribution-content and metadata tests covering the wheel, source distribution, `py.typed`,
  license files, Python support, and runtime dependencies.
- Add clean-environment wheel and source-distribution installation tests with import, typing-marker,
  metadata, and CDK synthesis smoke checks.
- Add explicit example-synthesis and dagitali.com consumer-compatibility layers to CI.
- Organize tests into unit, integration, end-to-end, and meta layers with shared helpers under
  `tests/support`.
- Add optional cdk-nag AWS Solutions checks with reviewed design-boundary acknowledgments.
- Add a manually approved, OIDC-authenticated disposable AWS deployment workflow with a fixed
  resource allowlist, unique stack name, cost boundaries, and automatic cleanup.
- Align pre-commit automation around the modern Ruff hook, the project-wide 88-character limit,
  standard test layers, and reusable Make-backed pre-push and manual CI gates.

## 0.2.9 - 2026-09-08

- Restore the omitted 0.2.8 release notes and add the versioned changelog section required for the
  corrective 0.2.9 release.

## 0.2.8 - 2026-09-08

- Update `actions/checkout` from 6.0.3 to 7.0.1 and `softprops/action-gh-release` from 3.0.0 to
  3.0.3 across the GitHub Actions workflows ([#3]).

## 0.2.7 - 2026-09-08

- Update the Python maintenance dependency constraints for `twine` and `setuptools-scm` to permit
  their latest compatible versions ([#2]).

## 0.2.6 - 2026-09-08

- Add focused, independently synthesizable examples for generated CloudFront hostnames, external
  DNS, Route 53, access logging, externally managed content, and customized security policy.
- Add a lightweight local Sphinx site with generated API documentation, strict CI validation, and
  deferred Read the Docs publication.
- Standardize reusable package-metadata conventions, including an explicit README media type,
  extensible author formatting, dependency-group intent, and a documentation source URL.
- Align reusable Make targets for strict local CI documentation checks, HTML and EPUB builds, link
  validation, and configurable documentation dependency installation.
- Harmonize reusable contributor, CI/CD, documentation, release-history, and repository-navigation
  guidance while retaining package-specific support and infrastructure boundaries.

## 0.2.5 - 2026-09-08

- Restore the omitted 0.2.4 release notes and add the versioned changelog section required by the
  tag-triggered release workflow.

## 0.2.4 - 2026-09-08

- Align the README release badge with GitHub Releases, clarify the architecture diagram, and update
  the installation example to the latest published tag.
- Clarify the pre-1.0 compatibility contract, supported public surface, and boundaries for support
  and vulnerability reporting.
- Standardize reusable README guidance for getting started, development, testing, coverage,
  quality checks, release validation, documentation, contributions, support, and licensing while
  retaining package-specific CDK guidance.

## 0.2.3 - 2026-09-08

- Make repository-local test support and package sources importable under both `pytest` and
  `python -m pytest` so the supported-version CI jobs use equivalent collection semantics.

## 0.2.2 - 2026-09-08

- Add pre-tag release-changelog validation to prevent publishing a tag without its matching dated
  changelog section.
- Record the `v0.2.1` changes without moving or reusing its existing public tag.

## 0.2.1 - 2026-09-08

- Automate tagged GitHub Releases with once-built distributions, isolated artifact smoke tests,
  SHA-256 checksums, and a CycloneDX SBOM.
- Harmonize reusable project documentation with the current release validation and publication
  lifecycle while preserving package-specific guidance.

## 0.2.0 - 2026-09-08

- Extract the initial site-agnostic construct from the dagitali.com CDK stack.
- Derive package versions from Git tags and enrich distribution metadata.
- Reject construct-managed certificate creation unless the stack explicitly targets `us-east-1`.
- Limit package installation to the Python 3.13 and 3.14 versions exercised by CI.
- Guard the logical IDs of stateful S3 resources against accidental replacement.
- Separate revalidated content and opt-in immutable-asset deployment cache policies.

[#2]: https://github.com/Dagitali/aws-cdk-static-site/pull/2
[#3]: https://github.com/Dagitali/aws-cdk-static-site/pull/3
