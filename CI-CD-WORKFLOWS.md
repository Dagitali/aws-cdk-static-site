# CI/CD Workflow Map

- [Scope](#scope)
- [Workflow Overview](#workflow-overview)
- [PR Gates](#pr-gates)
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

The shared Python-project baseline consists of `pr.yml`, `ci.yml`, `sbom.yml`, and `cd.yml`.
Repository-specific workflows extend that baseline without folding their responsibilities into the
four common lifecycle files.

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `.github/workflows/pr.yml` | Pull requests, merge queue | Enforce GitFlow pull-request routing |
| `.github/workflows/ci.yml` | Pull requests, protected-branch pushes, merge queue, manual | Validate source, tests, documentation, supported runtimes, and distributions |
| `.github/workflows/security.yml` | Manual | Run optional `cdk-nag` checks against synthesized infrastructure |
| `.github/workflows/deployment-test.yml` | Manual on `main` with protected environment | Create and destroy a bounded AWS test stack |
| `.github/workflows/sbom.yml` | Relevant protected-branch pushes, manual | Generate an advisory CycloneDX SBOM |
| `.github/workflows/cd.yml` | Semantic-version tag pushes or explicit historical backfill | Validate tagged artifacts and publish a GitHub Release |

PR policy, CI, and advisory SBOM generation run independently. Only a semantic-version tag triggers
release publication.

## PR Gates

Workflow name: `Pull Request (PR) Gates`

The `Guard pull request target` job enforces the documented GitFlow branch map. It also requires
release and hotfix pull requests targeting `main` to originate in this repository, matching the
shared production-safety boundary without requiring AWS access.

PR gates run for pull requests and merge-queue entries targeting `develop` or `main`. Comprehensive
source and package validation remains in `ci.yml`, keeping `pr.yml` focused on hosted pull-request
policy across projects.

## CI

Workflow name: `Continuous Integration (CI)`

The `Validate pull request` job verifies the dated changelog section for release and hotfix pull
requests, then runs the same `make check-pre-push` quality gate available to contributors and
agents. That gate verifies formatting, lint, types, repository policies, local Markdown links and
anchors, and tests with coverage (including example CDK synthesis), after which the job builds the
HTML documentation with warnings treated as errors. Separate `Build docs (epub)` and `Build docs
(linkcheck)` jobs validate a portable documentation artifact and external references. The `Test
Python … with … dependencies` matrix exercises every supported Python version against both the
lowest supported direct dependencies and the newest versions allowed by package metadata. `Validate
distributions` builds the wheel and sdist once, checks their contents, and installs each into a
clean environment. The advisory cross-platform jobs install the package and verify its public module
can be imported on macOS and Windows runners.

CI runs for pull requests and merge-queue entries targeting `develop` or `main`, pushes to those
branches, and manual dispatches.

Current-branch CI, security, and deployment-test jobs reuse
`.github/actions/setup-python-project/action.yml` for cached Python setup, project installation, and
`pip check` diagnostics. Release jobs intentionally remain self-contained because historical
backfills check out tags that may predate the local action. Remote actions inside workflows and the
composite action are covered by the repository's immutable-SHA policy check.

See the [testing guide] for local commands, test-layer boundaries, coverage behavior, and focused
suite execution.

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

Workflow name: `Continuous Deployment (CD)`

The `Build and validate release artifacts` job requires a dated changelog section matching the tag,
a corresponding `docs/releases/v<version>.md` document, and an entry for that document in the
release archive. Release and hotfix pull requests validate the same three records before merge. The
job then builds the sdist and wheel once, runs `twine check`, verifies distribution contents and
metadata, and installs each distribution into a separate clean environment for an import and basic
CDK synthesis test. It then generates SHA-256 checksums and a CycloneDX SBOM. The dependent `Publish
GitHub release` job waits for separate strict HTML and EPUB builds of the tagged documentation,
downloads the single validated artifact bundle, and attaches every file to the GitHub Release
associated with the existing tag.

Manual dispatch can recover a missing historical release by checking out an explicitly named,
existing annotated tag. Historical recovery never moves a tag or marks the backfilled release as
latest. The workflow does not create, move, or recreate tags and does not publish to PyPI.

## How the Workflows Interact

The workflows have distinct validation and publication responsibilities:

- `Pull Request (PR) Gates` enforces hosted pull-request routing.
- `Continuous Integration (CI)` provides source, test, documentation, compatibility, installation,
  synthesis, and distribution confidence gates.
- `Security checks` is an optional, credential-free infrastructure-policy review.
- `Test disposable AWS deployment` is a separately approved manual end-to-end check.
- `SBOM` is an advisory supply-chain artifact generated for relevant protected-branch changes.
- `Release` runs only for an explicit semantic-version tag and publishes GitHub assets after its
  artifact checks pass.
- No automatic workflow deploys AWS resources or publishes to PyPI.

## Required Checks

Protected branches should require `Guard pull request target`, `Validate pull request`, every `Test
Python … with … dependencies` matrix check, and `Validate distributions`. The guard runs in
`pr.yml`; validation, matrix, and distribution jobs run independently in `ci.yml`. Together these
checks cover branch routing, source validation, supported-version and dependency-boundary
compatibility, artifact contracts, and clean installation. Workflow step names are not status-check
names.

The EPUB and external-link documentation checks run for every pull request but are advisory by
default because external-link availability can be transient. Run `make check-ci-local`, `make
docs-epub`, and `make docs-linkcheck` to reproduce the package and documentation validation locally.
Platform-specific smoke jobs still require their corresponding GitHub-hosted runner or an equivalent
operating system.

When renaming workflows or jobs, follow the [required-check maintenance runbook] to stage the
replacement, observe its exact emitted name on a representative pull request, update the ruleset,
and verify enforcement. The [branch protection guide] remains the authoritative configuration.

[branch protection guide]: .github/BRANCH-PROTECTION.md
[deployment testing guide]: docs/runbooks/disposable-aws-deployment.md
[required-check maintenance runbook]: docs/runbooks/update-required-checks.md
[testing guide]: docs/TESTING.md
