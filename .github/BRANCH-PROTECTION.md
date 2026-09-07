# Branch Protection

This repository uses GitFlow-style branch roles:

- `feature/*` and `bugfix/*` branches start from and target `develop`.
- `chore/*`, `ci/*`, `docs/*`, and `dependabot/*` maintenance branches target
  `develop`.
- `sync/*` branches reconcile changes from `main` back into `develop`.
- `release/*` branches start from `develop` and target `main`.
- `hotfix/*` branches start from and target `main`, then synchronize back to
  `develop`.
- `develop` is the protected integration branch.
- `main` is the protected release branch and source of release tags.

- [Purpose](#purpose)
- [Recommended Required Checks](#recommended-required-checks)
- [Shared Protection Baseline](#shared-protection-baseline)
- [Branch-Specific Policy](#branch-specific-policy)
- [Protection Checklist for `develop`](#protection-checklist-for-develop)
- [Protection Checklist for `main`](#protection-checklist-for-main)
- [Preventing Direct Pushes](#preventing-direct-pushes)
- [Maintaining Required Checks](#maintaining-required-checks)
- [References](#references)

## Purpose

Branch protection makes GitHub the authoritative integration surface for long-lived branches. It
ensures that proposed changes follow the repository's branch map, pass repeatable validation, and
retain a reviewable pull-request record before `develop` or `main` moves.

## Recommended Required Checks

Require the `Validate package` and `Test on Python 3.14` status checks from
`.github/workflows/ci.yml`. Both depend on the `Guard PR target branch` job, so a valid pull-request
route, the package quality gate, and compatibility with each declared Python version must succeed.

The `Generate CycloneDX SBOM` job is advisory. It runs after relevant protected-branch pushes and
should not be configured as a pull-request requirement unless its workflow triggers are expanded to
cover every protected pull-request and merge-queue event.

## Shared Protection Baseline

Protect both `main` and `develop` with a GitHub ruleset that:

- Requires pull requests;
- Requires the `Validate package` and `Test on Python 3.14` status checks from
  `.github/workflows/ci.yml`, which depend on the `Guard PR target branch` job;
- Requires branches to be up to date before merging when merge queue is not enabled;
- Requires conversations to be resolved;
- Blocks force pushes and branch deletion;
- Prevents direct updates, including by administrators unless a documented
  recovery exception is necessary; and
- Dismisses stale approvals when review requirements are enabled.

For a solo-maintained project, required approval can remain disabled until another reviewer is
available, while pull requests and CI remain mandatory. Once multiple maintainers participate,
require at least one approval and CODEOWNERS review for governance, packaging, security, and
workflow changes.

## Branch-Specific Policy

Feature, bug-fix, routine maintenance, dependency, and synchronization pull requests target
`develop`. Only `release/*` and `hotfix/*` pull requests should target `main`. Release pull requests
document version changes, compatibility, validation, release notes, and rollback. Hotfix pull
requests document urgency and the plan to synchronize the correction back to `develop`.

Do not require a merge queue until every required workflow handles the `merge_group` event and a
representative queued pull request has succeeded. When enabling merge queue, review whether the
separate up-to-date branch requirement remains useful rather than retaining redundant controls by
default.

## Protection Checklist for `develop`

- [ ] Require pull requests and the `Validate package` and `Test on Python 3.14` status checks.
- [ ] Require branches to be up to date before merging unless merge queue is enabled.
- [ ] Require conversation resolution.
- [ ] Block force pushes, deletion, and direct updates.
- [ ] Accept routine topic branches and `sync/*` branches under the documented branch map.
- [ ] Add review and CODEOWNERS requirements when the maintainer team can satisfy them reliably.

## Protection Checklist for `main`

- [ ] Require pull requests and the `Validate package` and
  `Test on Python 3.14` status checks.
- [ ] Require branches to be up to date before merging unless merge queue is enabled.
- [ ] Require conversation resolution.
- [ ] Block force pushes, deletion, and direct updates.
- [ ] Accept only `release/*` and `hotfix/*` pull requests under the documented branch map.
- [ ] Restrict bypass permissions to documented recovery needs.

## Preventing Direct Pushes

Prefer repository rulesets targeted at `develop` and `main`. Require pull requests, disable force
pushes and deletions, and do not grant broad bypass access. If administrators or automation require
an exception, scope it narrowly, document why it exists, and test that ordinary users and tokens
cannot update either protected branch directly.

## Maintaining Required Checks

When a workflow or job name changes:

1. Run the new workflow successfully on a representative pull request.
2. Remove obsolete required-check names from the ruleset.
3. Add the exact new job name and select GitHub Actions as its source when available.
4. Confirm it runs for every protected target and supported merge event.

Workflow step names are not status-check names. This repository currently exposes the job names
`Validate package` and `Test on Python 3.14`. Run a representative pull request successfully before
adding a new job name to an active ruleset.

See the [CI/CD workflow map](../CI-CD-WORKFLOWS.md) for each workflow's public role and trigger
model.

Review the rulesets whenever branch names, workflow triggers, job names, merge-queue settings, or
maintainer roles change. A required check that does not run for every protected event can leave a
pull request permanently pending.

## References

- [GitHub rulesets](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-rulesets)
- [Protected branches](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-protected-branches)
- [Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/troubleshooting-required-status-checks)
