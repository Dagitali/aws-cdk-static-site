# Changelog

All notable changes to this project will be documented in this file.

- [Unreleased](#unreleased)
- [0.2.2 - 2026-09-08](#022---2026-09-08)
- [0.2.1 - 2026-09-08](#021---2026-09-08)
- [0.2.0 - 2026-09-08](#020---2026-09-08)

## Unreleased

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
