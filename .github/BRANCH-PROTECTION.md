# Branch Protection

This document defines a reusable branch-protection baseline and records the repository-specific
settings needed for this project. GitHub rulesets are preferred when available, although equivalent
branch protection rules may be used.

- [Purpose](#purpose)
- [Branch Roles](#branch-roles)
- [Required Status Checks](#required-status-checks)
  - [Selection Principles](#selection-principles)
  - [Repository-Specific Checks](#repository-specific-checks)
  - [Current Required-Check Candidates](#current-required-check-candidates)
  - [Current Advisory Checks](#current-advisory-checks)
- [Shared Protection Baseline](#shared-protection-baseline)
- [Repository-Specific Branch Settings](#repository-specific-branch-settings)
  - [`main`](#main)
  - [`develop`](#develop)
- [Disallowing Direct Updates](#disallowing-direct-updates)
- [Merge Queue](#merge-queue)
- [Updating Required Checks](#updating-required-checks)
- [Maintenance Notes](#maintenance-notes)
- [References](#references)

## Purpose

Protected branches should enforce these policies at the hosted-repository boundary:

- Changes reach protected branches through pull requests.
- Required validation succeeds before integration.
- Review requirements match the number of independent reviewers actually available.
- Review conversations are resolved before integration.
- Force pushes and branch deletion are blocked.
- Bypass access is absent or narrowly scoped and documented.

Local hooks provide earlier feedback but cannot replace server-side enforcement. Continuous
integration that runs after a direct push also cannot retroactively prevent that push.

When the repository's visibility or GitHub plan does not provide rulesets or branch protection,
treat this document as the target configuration rather than an active control. Do not imply that CI
prevents direct pushes in that state; retain the pull-request workflow voluntarily and reassess
server-side enforcement when repository access or plan capabilities change.

## Branch Roles

The protection principles apply regardless of language, build system, or branching model. Projects
that use trunk-based development, release branches, or another model should substitute their own
branch roles while retaining the review and validation requirements.

This repository uses GitFlow-style roles with hosted pull requests as the authoritative integration
path:

- `feature/*`: Feature and enhancement work. Create from and target `develop`.
- `bugfix/*`: Non-emergency corrections before release. Create from and target `develop`.
- `chore/*`, `ci/*`, `docs/*`, and `dependabot/*`: Focused maintenance work targeting `develop`.
- `sync/*`: Reconciliation from `main` back into `develop`.
- `release/*`: Release stabilization. Create from `develop` and target `main`.
- `hotfix/*`: Urgent corrections to the released line. Create from and target `main`.
- `support/*`: Maintainer-approved support for an older release line. Agree on its base and
  integration strategy before creating it, and update the target guard through a normal pull
  request before using the new path.

Do not use local Git Flow `finish` commands, such as `git flow feature finish`, `git flow release
finish`, or `git flow hotfix finish`, as the authoritative integration step. They typically perform
local merges and branch cleanup. Push working branches and merge them through hosted pull requests
instead.

After a release or hotfix reaches `main`, synchronize `main` back into `develop` through a pull
request so the integration branches do not diverge.

## Required Status Checks

Required checks should provide reliable evidence that a proposed change is safe to integrate. The
specific tools vary by project. Common categories include:

- Repository-policy and metadata validation.
- Formatting, linting, and static analysis.
- Automated tests on supported platforms and toolchains.
- Compilation, packaging, or infrastructure synthesis.
- Security, dependency, license, or artifact-integrity checks when their results are stable enough
  to block integration.

Do not require deployment or publication jobs that run only after a protected branch changes. Such
jobs cannot report a status on the pull request commit before merge.

### Selection Principles

- Require only checks that run for every pull request targeting the protected branch.
- Ensure required job names are unique across workflows. GitHub associates required checks with job
  names, not with a particular workflow or event.
- Select the exact check name emitted by a recent successful workflow run; step names are not status
  check names.
- Avoid making a path-filtered workflow required unless another mechanism reports the required check
  for excluded changes. A skipped workflow can otherwise leave a required check pending.
- Choose strict status checks when every topic branch must be current with its target before merge.
  Choose loose checks when fewer rebuilds are preferable and the integration risk is acceptable.
- If merge queue is required, ensure every required workflow handles the `merge_group` event.

Matrix jobs produce expanded check names. Confirm the names emitted by an actual workflow run rather
than copying the unexpanded matrix expression from workflow YAML.

### Repository-Specific Checks

The current workflow model is:

- `.github/workflows/pr.yml` runs for every pull request and merge group targeting `main` or
  `develop`. `Guard pull request target` enforces the GitFlow target rule and requires release and
  hotfix branches targeting `main` to originate in this repository.
- `.github/workflows/ci.yml` runs for every pull request and merge group targeting `main` or
  `develop`, for pushes to either protected branch, or when manually dispatched. `Validate pull
  request` performs policy, lint, type, test-with-coverage, synthesis, and documentation checks.
  Additional jobs exercise EPUB and external-link documentation builds, supported Python and
  dependency boundaries, cross-platform installation, and built distributions.
- `.github/workflows/cd.yml` builds and validates tagged package artifacts and publishes them to the
  corresponding GitHub Release. Manual dispatch supports recovery of an existing annotated tag.
- `.github/workflows/security.yml` and `.github/workflows/deployment-test.yml` are manually
  dispatched, repository-specific checks.
- `.github/workflows/sbom.yml` generates a Python dependency inventory after relevant pushes to
  `main` or `develop`, or when manually dispatched.

The PR and CI jobs have unique explicit names because GitHub required checks do not distinguish
identical job names by workflow. After the applicable jobs complete successfully on representative
pull requests, select their exact emitted check names in the ruleset.

Individual policy, lint, type-check, test-with-coverage, synthesis, and documentation entries are
steps inside the CI job. They are not independently selectable required checks. A project that needs
independent required results should place those checks in separately named jobs.

### Current Required-Check Candidates

After confirming their emitted names on a representative hosted run, these jobs are eligible to be
required for both protected branches:

- `Guard pull request target`
- `Validate pull request`
- `Test Python 3.13 with lowest dependencies`
- `Test Python 3.13 with newest dependencies`
- `Test Python 3.14 with lowest dependencies`
- `Test Python 3.14 with newest dependencies`
- `Validate distributions`

Treat the names as current repository configuration, not permanent policy. Refresh this list and the
hosted rulesets together whenever workflow job names or the supported Python matrix changes.

### Current Advisory Checks

These pull-request jobs provide useful additional evidence but are advisory by default:

- `Build docs (epub)`
- `Build docs (linkcheck)`
- `Smoke install on macos-latest`
- `Smoke install on windows-latest`

Cross-platform smoke checks depend on hosted-runner availability and can take longer than the core
gate. External-link availability can be transient. Promote an advisory job to a required check only
after it has proved reliable and continues to run for every applicable pull request and merge group.

Deployment, publication, manual security, and SBOM jobs must not be required because they do not run
for every pull request.

## Shared Protection Baseline

Apply this baseline to each protected integration branch:

- Require a pull request before changes can reach the branch.
- Require status checks to pass before merge.
- Require conversation resolution before merge.
- Dismiss stale approvals after review-relevant changes when independent review is required.
- Require Code Owner review only when a maintained `CODEOWNERS` file exists and an eligible reviewer
  is available.
- Block force pushes.
- Block branch deletion.
- Apply rules to administrators, or leave the bypass list empty, when operationally practical.
- If bypass access is necessary, grant it to the smallest appropriate set of maintainers or apps and
  prefer pull-request-only bypass where supported.

Require at least one approving review when an independent reviewer is routinely available. For a
solo-maintained repository, a mandatory approval can make ordinary pull requests impossible to merge
because authors cannot approve their own changes. In that case, require pull requests and status
checks with zero mandatory approvals, or document a narrowly scoped bypass policy.

Consider these optional protections according to project needs:

- Require the topic branch to be current with its target before merge.
- Require approval of the most recent reviewable push.
- Require a linear history when the allowed merge methods support it.
- Require signed commits after confirming contributor, bot, and merge-method compatibility.
- Require code scanning, dependency review, or successful staging deployment when those checks run
  reliably on every applicable change.
- Require merge queue when concurrent updates make merge-order conflicts common.

## Repository-Specific Branch Settings

### `main`

Purpose:

- Authoritative release history.
- Pull request target for `release/*` and `hotfix/*` branches.
- Source of annotated release tags and tag-triggered GitHub Releases.

Apply the shared baseline. Require the eligible PR and CI checks after representative runs establish
their exact names. Release pull requests should summarize release readiness, validation evidence,
compatibility impact, artifact effects, and rollback considerations. Hotfix pull requests should
also identify the affected release line and the plan to synchronize the correction back into
`develop`.

The repository does not automatically deploy AWS infrastructure from `main`. Tag-triggered release
publication is a post-merge control and is not a substitute for required pull-request checks.

### `develop`

Purpose:

- Protected integration history for work not yet released.
- Pull request target for feature, bugfix, maintenance, dependency, and synchronization branches.
- Source for `release/*` branches.

Apply the shared baseline and require the same eligible PR and CI checks. Pull requests should
remain focused, include appropriate test evidence, and identify intentional validation gaps.

## Disallowing Direct Updates

Prefer a repository ruleset when available:

1. Open repository **Settings**.
2. Open **Rules**, then **Rulesets**.
3. Create or edit a branch ruleset that targets the protected branches.
4. Set its enforcement status to **Active**.
5. Require pull requests and required status checks.
6. Require conversation resolution and the chosen review policy.
7. Restrict deletions and block force pushes.
8. Remove bypass actors, or grant only a documented, narrowly scoped exception.

If rulesets are unavailable, configure equivalent controls under **Settings**, **Branches**, and
**Branch protection rules**. Ensure administrators cannot silently bypass the policy unless that is
an intentional and documented recovery mechanism.

## Merge Queue

Do not enable merge queue until every required workflow supports the `merge_group` event and reports
the same required checks for queued merge groups. A workflow triggered only by `pull_request` does
not run automatically for a merge group.

The current `.github/workflows/ci.yml` and `.github/workflows/pr.yml` declare `merge_group`; their
required jobs report for merge groups. Any future required workflow must also support `merge_group`.

## Updating Required Checks

Whenever a workflow or job name changes:

1. Run the updated workflow successfully on a representative pull request.
2. Open the ruleset or branch protection rule for the target branch.
3. Remove stale or ambiguous required check names.
4. Add the exact current job name emitted by the successful run.
5. Select GitHub Actions as the expected source when that restriction is available.
6. Confirm the check runs for ordinary pull requests and every other required event.
7. Repeat for each protected branch that intentionally shares the policy.

Do not select workflow step names as required checks. If a required check remains pending, first
confirm that its workflow trigger, path filters, job conditions, and emitted name cover the current
pull request.

## Maintenance Notes

- Keep this file aligned with `.github/workflows/`, `.github/MAINTAINER-RUNBOOKS.md`,
  `CONTRIBUTING.md`, and the repository's actual rulesets or branch protection rules.
- Update branch-role guidance when the branching model changes.
- Keep required job names unique and update this document whenever they change.
- Treat platform, language, toolchain, and version-specific checks as repository-specific
  implementation details rather than permanent policy.
- Review bypass access periodically and remove exceptions that are no longer necessary.
- Test protections on a pull request after every material ruleset or workflow change.

## References

- [GitHub rules available for rulesets][ruleset-rules]
- [GitHub protected branch settings][protected-branches]
- [GitHub required-check troubleshooting][ruleset-troubleshooting]
- [GitHub merge queue configuration][merge-queue]

[merge-queue]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
[protected-branches]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
[ruleset-rules]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
[ruleset-troubleshooting]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules
