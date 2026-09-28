# Changelog

All notable changes to this project will be documented in this file. Detailed release-candidate
records are indexed in the [release notes archive].

- [Unreleased](#unreleased)
- [0.3.26 - 2026-09-27](#0326---2026-09-27)
- [0.3.25 - 2026-09-27](#0325---2026-09-27)
- [0.3.24 - 2026-09-27](#0324---2026-09-27)
- [0.3.23 - 2026-09-27](#0323---2026-09-27)
- [0.3.22 - 2026-09-27](#0322---2026-09-27)
- [0.3.21 - 2026-09-20](#0321---2026-09-20)
- [0.3.20 - 2026-09-20](#0320---2026-09-20)
- [0.3.19 - 2026-09-20](#0319---2026-09-20)
- [0.3.18 - 2026-09-17](#0318---2026-09-17)
- [0.3.17 - 2026-09-17](#0317---2026-09-17)
- [0.3.16 - 2026-09-17](#0316---2026-09-17)
- [0.3.15 - 2026-09-17](#0315---2026-09-17)
- [0.3.14 - 2026-09-15](#0314---2026-09-15)
- [0.3.13 - 2026-09-15](#0313---2026-09-15)
- [0.3.12 - 2026-09-15](#0312---2026-09-15)
- [0.3.11 - 2026-09-15](#0311---2026-09-15)
- [0.3.10 - 2026-09-10](#0310---2026-09-10)
- [0.3.9 - 2026-09-10](#039---2026-09-10)
- [0.3.8 - 2026-09-10](#038---2026-09-10)
- [0.3.7 - 2026-09-10](#037---2026-09-10)
- [0.3.6 - 2026-09-10](#036---2026-09-10)
- [0.3.5 - 2026-09-09](#035---2026-09-09)
- [0.3.4 - 2026-09-09](#034---2026-09-09)
- [0.3.3 - 2026-09-09](#033---2026-09-09)
- [0.3.2 - 2026-09-08](#032---2026-09-08)
- [0.3.1 - 2026-09-08](#031---2026-09-08)
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
- [0.1.4 - 2026-09-08](#014---2026-09-08)
- [0.1.3 - 2026-09-08](#013---2026-09-08)
- [0.1.2 - 2026-09-07](#012---2026-09-07)
- [0.1.1 - 2026-09-07](#011---2026-09-07)
- [0.1.0 - 2026-09-07](#010---2026-09-07)
- [0.0.0 - 2026-09-06](#000---2026-09-06)

## [Unreleased]

## [0.3.26] - 2026-09-27

- Update the full-SHA pin for `aws-actions/configure-aws-credentials` from v6.2.4 to v6.3.0 in the
  manual disposable AWS deployment test, preserving its existing inputs, permissions, environment
  gate, and cleanup safeguards ([#8]).

## [0.3.25] - 2026-09-27

- Standardize file headers, release-summary wording, present-tense highlights, and verified tag-date
  introductions across the release archive while preserving version-specific compatibility and
  operational details.
- Add direct changelog, archive, and release-policy navigation and complete historical records'
  validation sections and tables of contents.
- Distinguish historical preparation checks from verified tagging and publication evidence without
  attributing current-checkout validation to earlier releases.

## [0.3.24] - 2026-09-27

- Raise the minimum supported `aws-cdk-lib` version from 2.269.0 to 2.271.0 and align the
  deterministic lowest-dependency constraint with the published package metadata.
- Refresh the minimum supported versions of the development, documentation, and optional security
  tools used by contributors and CI.

## [0.3.23] - 2026-09-27

- Remove the unused `write_file` pytest fixture, its `FileWriter` support type, and the obsolete
  testing guidance that referenced them.
- Expand invalid content-path coverage to verify that deployment rejects both missing paths and
  existing files.
- Run the release-changelog quality gate with the project environment's Python interpreter so it
  uses the pinned Popo installation consistently with the other repository-policy checks.

## [0.3.22] - 2026-09-27

- Adopt the pinned Popo CLI as the authoritative implementation for repository-policy checks in
  Make, pre-commit, pull-request validation, and tagged-release validation, with explicit consumer
  configuration in `pyproject.toml`.
- Remove the deprecated repository-local `scripts` policy package and its direct tests after the
  Popo-backed quality gates completed their migration window.

## [0.3.21] - 2026-09-20

- Strengthen Markdown-checker regression coverage for repositories beneath hidden parent
  directories, `.github` documentation, generated-directory exclusions, and fenced code blocks.

## [0.3.20] - 2026-09-20

- Add direct contract tests for the shared Python-project setup action's boolean inputs, early
  validation, conditional installation, dependency check, and step ordering.
- Add reusable, privacy-aware evidence inventory and documentation-correction intake templates for
  verifying public technical claims without exposing confidential material.
- Add direct regression tests for Make cleanup path guards and overridable installation, formatting,
  and unit-test commands.
- Centralize repository-root discovery in a session-scoped test fixture shared by project-level
  contract suites.
- Add a reusable change-management playbook connecting scope classification, operable scaffolding,
  documentation synchronization, release evidence, and rollback boundaries.
- Simplify pull-request routing so `develop` accepts canonical, repository-specific, automated, and
  external branch names while `main` remains restricted to same-repository release and hotfix
  branches; distinguish canonical Git Flow roles from optional repository prefixes in contributor
  guidance.
- Add role-oriented documentation navigation and separate guide and topic indexes without changing
  the package's canonical source or operating boundaries.

## [0.3.19] - 2026-09-20

- Add a deterministic repository-wide Markdown link and heading-anchor check to the shared
  maintenance CLI, Make quality gate, and pre-commit configuration, and repair the stale Learnings
  table-of-contents anchor it detected.
- Align the pull-request template with shared documentation-decision and agent-safety review prompts
  while retaining package-specific compatibility checks.
- Add a package-specific developer-onboarding guide using the same reusable structure as the
  consumer site while keeping credential-free synthesis and package compatibility boundaries clear.
- Validate composite-action boolean inputs before environment setup, and add direct unit contracts
  for shared maintenance helpers.
- Align reusable contribution, agent, tutorial, runbook, and security guidance around privacy,
  accessibility, confidential evidence, and explicit authorization for DNS or AWS changes.
- Standardize ADR metadata and release evidence around dates, supersession, verification, artifacts,
  infrastructure diffs, and explicit deployment, publication, DNS, or replacement impact.
- Document the construct's verified security model, enforced controls, consumer responsibilities,
  deliberate exclusions, and credential boundary in the public security policy.

## [0.3.18] - 2026-09-17

- Raise the minimum supported `aws-cdk-lib` version from 2.267.0 to 2.269.0 and align the
  deterministic lowest-dependency test constraint with the published package metadata ([#4]).

## [0.3.17] - 2026-09-17

- Centralize cached Python setup, project installation, and dependency diagnostics in a reusable
  local GitHub Action shared by current-branch CI, security, and deployment-test workflows.
- Align hosted and local quality gates around deterministic Make targets, and extend immutable
  GitHub Actions pin validation to workflow and composite-action YAML with canonical commands and
  deprecated compatibility aliases.

## [0.3.16] - 2026-09-17

- Require release and hotfix pull requests plus tagged continuous delivery to verify the matching
  dated changelog section, versioned release document, and release-archive entry before publication.

## [0.3.15] - 2026-09-17

- Establish a comprehensive, cross-linked documentation system covering architecture, design
  decisions, project planning, contributor workflows, operations, consumer adoption, and releases.
- Organize maintained guidance into indexed API, architecture, decision, development, playbook,
  runbook, tutorial, and release sections without changing package or infrastructure behavior.

## [0.3.14] - 2026-09-15

- Isolate Sphinx doctrees from builder output in CI and tagged-release documentation jobs so strict
  EPUB validation does not misclassify internal build-state files as package content.

## [0.3.13] - 2026-09-15

- Standardize the four shared Python-project workflows and their supporting GitHub governance
  documents around the same reusable responsibilities, naming, templates, and maintainer guidance
  used by sibling Dagitali projects, adding EPUB and link-check CI plus tagged HTML and EPUB release
  validation, explicit required and advisory check guidance, and consistent release-note practices
  while retaining this package's compatibility, infrastructure, and artifact safeguards.

## [0.3.12] - 2026-09-15

- Update the `ruff-pre-commit` hook from 0.16.6 to 0.16.7, incorporating upstream correctness and
  performance improvements while retaining the repository's existing Ruff rules and hook behavior
  ([#6]).

## [0.3.11] - 2026-09-15

- Update the deployment-test workflow's immutable `aws-actions/configure-aws-credentials` pin from
  6.2.3 to 6.2.4, incorporating upstream fixes for account-ID handling, proxy-secret masking, and
  final retry backoff ([#5]).

## [0.3.10] - 2026-09-10

- Reorganize the README around consistent getting-started, release-status, quickstart, support, and
  documentation sections, and correct the quickstart's construct assignment.
- Add repository funding metadata and sponsorship guidance for ongoing maintenance, compatibility,
  documentation, and release work.
- Standardize reference-style links across maintained project documentation while retaining direct
  links in the dedicated reference catalog.

## [0.3.9] - 2026-09-10

- Replace the README's version-specific installation command with a stable release-tag placeholder
  and remove its obsolete updater, tests, Make targets, checklist steps, and CI/CD gates.
- Replace duplicated Python-version and CI-matrix details with references to canonical project
  metadata, and correct stale branch-protection, runbook, and package-adoption guidance.
- Refresh SBOM workflow action annotations while retaining immutable action pins.

## [0.3.8] - 2026-09-10

- Update the README installation example to reference the current release tag so tagged-release
  validation succeeds.

## [0.3.7] - 2026-09-10

- Consolidate repository-maintenance utilities behind shared support and a verb-oriented `python -m
  scripts` command-line interface used by Make, pre-commit, and GitHub Actions.
- Reject duplicate dependency declarations and reversed README markers, with expanded regression
  coverage for repository-policy utilities.

## [0.3.6] - 2026-09-10

- Add Python 3.13 and 3.14 CI coverage for both the lowest supported direct dependencies and the
  newest versions permitted by package metadata, with a drift check for minimum constraints.

## [0.3.5] - 2026-09-09

- Expand Python module, public API, repository utility, fixture, and test-suite docstrings using
  NumPy conventions, with richer generated documentation for construct configuration and outputs.

## [0.3.4] - 2026-09-09

- Configure Ruff to prefer single quotes, including nested Python 3.13 f-string expressions.
- Apply the enforced formatting consistently across Python code and documentation examples without
  changing package behavior.

## [0.3.3] - 2026-09-09

- Remove the private `dagitali.com` checkout, consumer-specific integration test, and corresponding
  CI and Make targets, keeping reusable-package validation self-contained.
- Align testing, contribution, workflow, and branch-protection documentation with the simplified
  validation boundary.
- Run local Python-policy and workflow-pin checks in pre-commit-managed environments so graphical
  Git clients cannot select an unsupported system interpreter through a restricted `PATH`.
- Repair release distribution validation by installing the pytest coverage plugin required by the
  repository's configured test arguments.
- Add an exact-tag manual recovery path for missing historical GitHub Releases while preventing
  backfills from becoming the latest release.
- Generate and validate the README's versioned GitHub installation snippet during release
  preparation and tagged publication.

## [0.3.2] - 2026-09-08

- Authenticate the consumer-compatibility job with a dedicated read-only token so CI can check out
  the private `Dagitali/dagitali.com` repository, fail clearly when the token is absent, and avoid
  persisting its credentials.

## [0.3.1] - 2026-09-08

- Install the optional security dependencies in the primary CI job before mypy checks the complete
  test tree, preventing missing-import failures for `cdk_nag`.

## [0.3.0] - 2026-09-08

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

## [0.2.9] - 2026-09-08

- Restore the omitted 0.2.8 release notes and add the versioned changelog section required for the
  corrective 0.2.9 release.

## [0.2.8] - 2026-09-08

- Update `actions/checkout` from 6.0.3 to 7.0.1 and `softprops/action-gh-release` from 3.0.0 to
  3.0.3 across the GitHub Actions workflows ([#3]).

## [0.2.7] - 2026-09-08

- Update the Python maintenance dependency constraints for `twine` and `setuptools-scm` to permit
  their latest compatible versions ([#2]).

## [0.2.6] - 2026-09-08

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

## [0.2.5] - 2026-09-08

- Restore the omitted 0.2.4 release notes and add the versioned changelog section required by the
  tag-triggered release workflow.

## [0.2.4] - 2026-09-08

- Align the README release badge with GitHub Releases, clarify the architecture diagram, and update
  the installation example to the latest published tag.
- Clarify the pre-1.0 compatibility contract, supported public surface, and boundaries for support
  and vulnerability reporting.
- Standardize reusable README guidance for getting started, development, testing, coverage, quality
  checks, release validation, documentation, contributions, support, and licensing while retaining
  package-specific CDK guidance.

## [0.2.3] - 2026-09-08

- Make repository-local test support and package sources importable under both `pytest` and `python
  -m pytest` so the supported-version CI jobs use equivalent collection semantics.

## [0.2.2] - 2026-09-08

- Add pre-tag release-changelog validation to prevent publishing a tag without its matching dated
  changelog section.
- Record the `v0.2.1` changes without moving or reusing its existing public tag.

## [0.2.1] - 2026-09-08

- Automate tagged GitHub Releases with once-built distributions, isolated artifact smoke tests,
  SHA-256 checksums, and a CycloneDX SBOM.
- Harmonize reusable project documentation with the current release validation and publication
  lifecycle while preserving package-specific guidance.

## [0.2.0] - 2026-09-08

- Extract the initial site-agnostic construct from the dagitali.com CDK stack.
- Derive package versions from Git tags and enrich distribution metadata.
- Reject construct-managed certificate creation unless the stack explicitly targets `us-east-1`.
- Limit package installation to the Python 3.13 and 3.14 versions exercised by CI.
- Guard the logical IDs of stateful S3 resources against accidental replacement.
- Separate revalidated content and opt-in immutable-asset deployment cache policies.

## [0.1.4] - 2026-09-08

- Add selective logical-ID regression assertions for stateful S3 resources while retaining
  property-based assertions for resources without replacement-sensitive identities.

## [0.1.3] - 2026-09-08

- Establish Python 3.13 and 3.14 as the tested support range across package metadata, tooling, CI,
  validation, and documentation.

## [0.1.2] - 2026-09-07

- Reject construct-managed CloudFront certificate creation outside `us-east-1`, with synthesis-time
  validation, regression coverage, and configuration guidance.

## [0.1.1] - 2026-09-07

- Improve project discoverability with release, Python, license, and CI badges plus a concise
  architecture diagram for the S3 and CloudFront delivery path.

## [0.1.0] - 2026-09-07

- Add the initial typed `StaticSite` construct with private S3 storage, CloudFront delivery,
  security headers, optional content deployment, custom domains, access logging, and Route 53
  integration.
- Establish the package layout, basic example, tests, CI and SBOM workflows, maintenance checks,
  contributor guidance, security policy, and release documentation.

## [0.0.0] - 2026-09-06

- Establish the repository shell with the project README, MIT license, Git ignore rules, and
  intended reusable static-site scope.

[#2]: https://github.com/Dagitali/aws-cdk-static-site/pull/2
[#3]: https://github.com/Dagitali/aws-cdk-static-site/pull/3
[#4]: https://github.com/Dagitali/aws-cdk-static-site/pull/4
[#5]: https://github.com/Dagitali/aws-cdk-static-site/pull/5
[#6]: https://github.com/Dagitali/aws-cdk-static-site/pull/6
[#8]: https://github.com/Dagitali/aws-cdk-static-site/pull/8
[Unreleased]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.26...HEAD
[0.3.26]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.25...v0.3.26
[0.3.25]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.24...v0.3.25
[0.3.24]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.23...v0.3.24
[0.3.23]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.22...v0.3.23
[0.3.22]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.21...v0.3.22
[0.3.21]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.20...v0.3.21
[0.3.20]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.19...v0.3.20
[0.3.19]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.18...v0.3.19
[0.3.18]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.17...v0.3.18
[0.3.17]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.16...v0.3.17
[0.3.16]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.15...v0.3.16
[0.3.15]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.14...v0.3.15
[0.3.14]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.13...v0.3.14
[0.3.13]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.12...v0.3.13
[0.3.12]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.11...v0.3.12
[0.3.11]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.10...v0.3.11
[0.3.10]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.9...v0.3.10
[0.3.9]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.9...v0.3.0
[0.2.9]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.8...v0.2.9
[0.2.8]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.7...v0.2.8
[0.2.7]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.6...v0.2.7
[0.2.6]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Dagitali/aws-cdk-static-site/compare/v0.0.0...v0.1.0
[0.0.0]: https://github.com/Dagitali/aws-cdk-static-site/releases/tag/v0.0.0
[release notes archive]: docs/releases/README.md
