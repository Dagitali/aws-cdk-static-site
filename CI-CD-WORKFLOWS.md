# CI/CD Workflow Map

- [Scope](#scope)
- [Workflow Overview](#workflow-overview)
- [CI](#ci)
- [Security Checks](#security-checks)
- [Disposable AWS Deployment Test](#disposable-aws-deployment-test)
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
| `.github/workflows/security.yml` | Manual | Run optional `cdk-nag` checks against synthesized infrastructure |
| `.github/workflows/deployment-test.yml` | Manual on `main` with protected environment | Create and destroy a bounded AWS test stack |
| `.github/workflows/sbom.yml` | Relevant protected-branch pushes, manual | Generate an advisory CycloneDX SBOM |
| `.github/workflows/cd.yml` | Semantic-version tag pushes or explicit historical backfill | Validate tagged artifacts and publish a GitHub Release |

CI and advisory SBOM generation run independently. Only a semantic-version tag triggers release
publication.

## CI

Workflow name: `CI`

The `Guard PR target branch` job enforces the documented GitFlow branch map. The dependent `Validate
package` job verifies the dated changelog section for release and hotfix pull requests before it
installs development dependencies, lints, type-checks, verifies repository policies, runs unit tests
with coverage, and builds the HTML documentation with warnings treated as errors. The dependent
`Test Python … with … dependencies` matrix exercises every supported Python version against both the
lowest supported direct dependencies and the newest versions allowed by package metadata. `Validate
distributions` builds the wheel and sdist once, checks their contents, and installs each into a
clean environment. The advisory cross-platform jobs install the package and verify its public module
can be imported on macOS and Windows runners.

CI runs for pull requests and merge-queue entries targeting `develop` or `main`, pushes to those
branches, and manual dispatches.

## Security Checks

Workflow name: `Security checks`

The manual `Check synthesized security findings` job installs the optional `security` dependency
group and runs the `cdk-nag` AWS Solutions baseline. The test acknowledges only documented
consumer-owned geo-restriction, WAF, and S3 server-access-logging decisions; any other finding fails
the job. It synthesizes locally and requires no AWS credentials.

## Disposable AWS Deployment Test

Workflow name: `Test disposable AWS deployment`

The manual workflow runs only from `main` after an exact confirmation and approval through the
`deployment-test` GitHub environment. It uses OIDC credentials, validates a fixed resource
allowlist, creates a uniquely named empty stack, verifies it, and waits for deletion. It is never a
routine CI or release prerequisite. See the [deployment testing guide].

## SBOM

Workflow name: `SBOM`

The `Generate CycloneDX SBOM` job creates and validates a dependency SBOM, then uploads it as a
short-lived workflow artifact. It runs after relevant package or workflow changes are pushed to
`develop` or `main`, and by manual dispatch. It does not attest to a deployed AWS environment or
replace review of synthesized CloudFormation.

## Release

Workflow name: `Release`

The `Build and validate release artifacts` job requires a dated changelog section matching the tag.
It builds the sdist and wheel once, runs `twine check`, verifies distribution contents and metadata,
and installs each distribution into a separate clean environment for an import and basic CDK
synthesis test. It then generates SHA-256 checksums and a CycloneDX SBOM. The dependent `Publish
GitHub release` job downloads that single validated artifact bundle and attaches every file to the
GitHub Release associated with the existing tag.

Manual dispatch can recover a missing historical release by checking out an explicitly named,
existing annotated tag. Historical recovery never moves a tag or marks the backfilled release as
latest. The workflow does not create, move, or recreate tags and does not publish to PyPI.

## How the Workflows Interact

The workflows have distinct validation and publication responsibilities:

- `CI` is the required confidence gate for protected-branch integration.
- `Security checks` is an optional, credential-free infrastructure-policy review.
- `Test disposable AWS deployment` is a separately approved manual end-to-end check.
- `SBOM` is an advisory supply-chain artifact generated for relevant protected-branch changes.
- `Release` runs only for an explicit semantic-version tag and publishes GitHub assets after its
  artifact checks pass.
- No automatic workflow deploys AWS resources or publishes to PyPI.

## Required Checks

Protected branches should require `Validate package`, every `Test Python … with … dependencies`
matrix check, and `Validate distributions`. These jobs depend on `Guard PR target branch`, so source
validation, supported-version and dependency-boundary compatibility, artifact contracts, clean
installation, and branch routing must succeed. Workflow step names are not status-check names.

Run `make check-ci-local` to reproduce the primary package validation and strict HTML documentation
build locally. Platform-specific smoke jobs still require their corresponding GitHub-hosted runner
or an equivalent operating system.

When renaming workflows or jobs, run the replacement on a representative pull request before
updating the ruleset. See the [branch protection guide].

[branch protection guide]: .github/BRANCH-PROTECTION.md
[deployment testing guide]: docs/DEPLOYMENT-TESTING.md
