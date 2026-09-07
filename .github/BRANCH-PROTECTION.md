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

- [Shared Protection Baseline](#shared-protection-baseline)
- [Branch-Specific Policy](#branch-specific-policy)
- [Maintaining Required Checks](#maintaining-required-checks)
- [References](#references)

## Shared Protection Baseline

Protect both `main` and `develop` with a GitHub ruleset that:

- requires pull requests;
- requires the `Validate package` status check from `.github/workflows/ci.yml`,
  which depends on the `Guard PR target branch` job;
- requires conversations to be resolved;
- blocks force pushes and branch deletion;
- prevents direct updates, including by administrators unless a documented
  recovery exception is necessary; and
- dismisses stale approvals when review requirements are enabled.

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
representative queued pull request has succeeded.

## Maintaining Required Checks

When a workflow or job name changes:

1. Run the new workflow successfully on a representative pull request.
2. Remove obsolete required-check names from the ruleset.
3. Add the exact new job name and select GitHub Actions as its source when available.
4. Confirm it runs for every protected target and supported merge event.

Workflow step names are not status-check names. This repository currently exposes
the job name `Validate package`.

See the [CI/CD workflow map](../CI-CD-WORKFLOWS.md) for each workflow's public role and trigger
model.

## References

- [GitHub rulesets](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-rulesets)
- [Protected branches](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/about-protected-branches)
- [Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/troubleshooting-required-status-checks)
