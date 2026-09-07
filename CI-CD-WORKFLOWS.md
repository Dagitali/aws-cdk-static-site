# CI/CD Workflow Map

- [Scope](#scope)
- [Workflow Overview](#workflow-overview)
- [CI](#ci)
- [SBOM](#sbom)
- [How the Workflows Interact](#how-the-workflows-interact)
- [Required Checks](#required-checks)
- [Future Release Automation](#future-release-automation)

## Scope

This document describes the public roles and triggers of repository workflows. It excludes secrets,
credential handling, emergency access, and other private operator procedures.

## Workflow Overview

Automation is separated by responsibility:

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Pull requests, protected-branch pushes, merge queue, manual | Validate the package, supported Python versions, and GitFlow target |
| `.github/workflows/sbom.yml` | Relevant protected-branch pushes, manual | Generate an advisory CycloneDX SBOM |

These workflows run independently. SBOM generation is supplementary and is not a publication
trigger.

## CI

Workflow name: `CI`

The `Guard PR target branch` job enforces the documented GitFlow branch map. The dependent `Validate
package` job installs development dependencies, lints, type-checks, verifies repository policies,
runs unit tests with coverage, and builds and checks distributions. The dependent `Test on Python
3.14` job verifies compatibility with the additional Python version declared by the package
metadata. The advisory cross-platform jobs install the package and verify its public module can be
imported on macOS and Windows runners.

CI runs for pull requests and merge-queue entries targeting `develop` or `main`, pushes to those
branches, and manual dispatches.

## SBOM

Workflow name: `SBOM`

The `Generate CycloneDX SBOM` job creates and validates a dependency SBOM, then uploads it as a
short-lived workflow artifact. It runs after relevant package or workflow changes are pushed to
`develop` or `main`, and by manual dispatch. It does not attest to a deployed AWS environment or
replace review of synthesized CloudFormation.

## How the Workflows Interact

The workflows do not form a publication pipeline:

- `CI` is the required confidence gate for protected-branch integration.
- `SBOM` is an advisory supply-chain artifact generated for relevant protected-branch changes.
- Neither workflow deploys AWS resources or publishes a Python package.
- A future release workflow must use an explicit release trigger rather than treating an ordinary
  successful CI run as authorization to publish.

## Required Checks

Protected branches should require `Validate package` and `Test on Python 3.14`. Both jobs depend on
`Guard PR target branch`, so package validation, supported-version compatibility, and the
branch-routing policy must succeed. Workflow step names are not status-check names.

When renaming workflows or jobs, run the replacement on a representative pull request before
updating the ruleset. See [.github/BRANCH-PROTECTION.md](.github/BRANCH-PROTECTION.md).

## Future Release Automation

The project does not yet define tag-triggered publication. Before adding it, require artifact
validation, clean-environment wheel smoke tests, a protected GitHub environment, and PyPI trusted
publishing without long-lived credentials. Keep CI validation separate from the explicit release
trigger.
