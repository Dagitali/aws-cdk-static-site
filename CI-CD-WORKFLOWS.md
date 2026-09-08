# CI/CD Workflow Map

- [Scope](#scope)
- [Workflow Overview](#workflow-overview)
- [CI](#ci)
- [SBOM](#sbom)
- [Release](#release)
- [How the Workflows Interact](#how-the-workflows-interact)
- [Required Checks](#required-checks)

## Scope

This document describes the public roles and triggers of repository workflows. It excludes secrets,
credential handling, emergency access, and other private operator procedures.

## Workflow Overview

Automation is separated by responsibility:

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Pull requests, protected-branch pushes, merge queue, manual | Validate the package, supported Python versions, and GitFlow target |
| `.github/workflows/sbom.yml` | Relevant protected-branch pushes, manual | Generate an advisory CycloneDX SBOM |
| `.github/workflows/cd.yml` | Semantic-version tag pushes | Validate artifacts and publish a GitHub Release |

CI and advisory SBOM generation run independently. Only a semantic-version tag triggers release
publication.

## CI

Workflow name: `CI`

The `Guard PR target branch` job enforces the documented GitFlow branch map. The dependent `Validate
package` job verifies the dated changelog section for release and hotfix pull requests before it
installs development dependencies, lints, type-checks, verifies repository policies, runs unit tests
with coverage, and builds and checks distributions. The dependent `Test on Python 3.14` job verifies
compatibility with the additional Python version declared by the package metadata. The advisory
cross-platform jobs install the package and verify its public module can be imported on macOS and
Windows runners.

CI runs for pull requests and merge-queue entries targeting `develop` or `main`, pushes to those
branches, and manual dispatches.

## SBOM

Workflow name: `SBOM`

The `Generate CycloneDX SBOM` job creates and validates a dependency SBOM, then uploads it as a
short-lived workflow artifact. It runs after relevant package or workflow changes are pushed to
`develop` or `main`, and by manual dispatch. It does not attest to a deployed AWS environment or
replace review of synthesized CloudFormation.

## Release

Workflow name: `Release`

The `Build and validate release artifacts` job requires a dated changelog section matching the tag,
builds the sdist and wheel once, runs `twine check`, and installs each distribution into a separate
clean environment for an import and basic CDK synthesis test. It then generates SHA-256 checksums
and a CycloneDX SBOM. The dependent `Publish GitHub release` job downloads that single validated
artifact bundle and attaches every file to the GitHub Release associated with the existing tag.

The workflow does not create, move, or recreate tags and does not publish to PyPI.

## How the Workflows Interact

The workflows have distinct validation and publication responsibilities:

- `CI` is the required confidence gate for protected-branch integration.
- `SBOM` is an advisory supply-chain artifact generated for relevant protected-branch changes.
- `Release` runs only for an explicit semantic-version tag and publishes GitHub assets after its
  artifact checks pass.
- No workflow deploys AWS resources or publishes to PyPI.

## Required Checks

Protected branches should require `Validate package` and `Test on Python 3.14`. Both jobs depend on
`Guard PR target branch`, so package validation, supported-version compatibility, and the
branch-routing policy must succeed. Workflow step names are not status-check names.

When renaming workflows or jobs, run the replacement on a representative pull request before
updating the ruleset. See [.github/BRANCH-PROTECTION.md](.github/BRANCH-PROTECTION.md).
