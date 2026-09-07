# Maintainer Runbooks

- [Operating Model](#operating-model)
- [Start Repository Work](#start-repository-work)
- [Develop a Feature or Bug Fix](#develop-a-feature-or-bug-fix)
- [Prepare a Release](#prepare-a-release)
- [Apply a Hotfix](#apply-a-hotfix)
- [Synchronize `main` Back to `develop`](#synchronize-main-back-to-develop)
- [Tag a Release](#tag-a-release)
- [Investigate Failed Checks](#investigate-failed-checks)
- [Recover a Release](#recover-a-release)
- [Clean Up](#clean-up)
- [Solo-Maintainer Notes](#solo-maintainer-notes)
- [Keep Private Elsewhere](#keep-private-elsewhere)

## Operating Model

Working branches hold proposed changes; protected branches move through GitHub pull requests.
`develop` is the integration branch, `main` is the release branch, and annotated release tags point
to authoritative commits already merged into `main`.

Use `git flow ... start` or equivalent Git commands to create working branches. Do not use
`git flow ... finish` as the authoritative integration or cleanup operation because it performs
local merges outside the protected pull-request surface.

## Start Repository Work

1. Confirm the intended change and target branch.
2. Preserve unrelated working-tree changes.
3. Fetch remote references and update the appropriate protected base with a fast-forward-only pull.
4. Create a focused branch using the documented GitFlow branch families in
   `.github/BRANCH-PROTECTION.md`.
5. Install development dependencies and hooks, then run `make check`.

Do not use local Git Flow `finish` commands as the authoritative integration step. Merge through a
GitHub pull request and clean up branches afterward.

## Develop a Feature or Bug Fix

1. Start from current `develop`.
2. Implement one cohesive change with tests and documentation.
3. Update `CHANGELOG.md` for user-visible behavior.
4. Run `make check` and push the topic branch.
5. Open a pull request targeting `develop` and complete required checks.

## Prepare a Release

Use the public [release checklist](../RELEASE-CHECKLIST.md) together with these repository-specific
steps. The versioning and compatibility rules are defined in
[RELEASE-POLICY.md](../RELEASE-POLICY.md).

1. Confirm `develop` contains the intended scope and passes CI.
2. Create `release/<version>` from `develop`.
3. Finalize `CHANGELOG.md`, and review the public API and compatibility impact. Do not edit a
   package version: `setuptools-scm` derives it from Git tags.
4. Build the sdist and wheel, run `twine check`, and install the wheel into a clean environment for
   a preliminary import and synthesis smoke test.
5. Open a pull request targeting `main` and merge through GitHub.
6. Create an annotated `v<version>` tag on the authoritative merged `main` commit.
7. Check out the tag, build the authoritative release distributions, verify that their derived
   version matches the tag, and repeat the clean-environment smoke test.
8. Synchronize `main` back into `develop` through a pull request.

The repository does not yet publish to PyPI. Do not upload a package manually or configure
publishing credentials until a reviewed release workflow and protected PyPI environment exist.

## Apply a Hotfix

1. Start `hotfix/<version>` from current `main`.
2. Make the smallest safe correction and add regression coverage.
3. Run the full package gate and document compatibility and rollback.
4. Open a pull request targeting `main`.
5. Tag the merged commit only if it represents a release.
6. Synchronize the merged fix back to `develop` through a pull request.

## Synchronize `main` Back to `develop`

After every release or hotfix:

1. Fetch current remote state for `main` and `develop`.
2. Create `sync/main-into-develop` from current `develop`.
3. Merge `origin/main` into the sync branch and resolve conflicts there.
4. Run `make check`.
5. Push the sync branch and open a pull request targeting `develop`.
6. Merge through GitHub after required checks pass.

## Tag a Release

1. Fetch the merged remote `main` commit.
2. Confirm the commit contains the intended changelog and release scope.
3. Create an annotated `vMAJOR.MINOR.PATCH` tag on that exact commit.
4. Verify the tag target and annotation locally.
5. Push the tag once; never move or reuse a published version.

The [release policy](../RELEASE-POLICY.md) defines version semantics, and the
[release checklist](../RELEASE-CHECKLIST.md) defines the complete readiness gate.

## Investigate Failed Checks

1. Identify the first meaningful failing step.
2. Reproduce it locally when practical.
3. Correct the cause and add regression coverage.
4. Rerun unchanged jobs only when evidence indicates a transient failure.
5. Do not weaken a required check merely to merge a change.

## Recover a Release

Prefer a corrective release or a reviewed revert over moving a published tag. Never reuse a
published version. If a package is eventually published, follow PyPI's release and yanking semantics
and document the consumer impact.

## Clean Up

After confirming the authoritative merge, delete the remote topic branch, prune remote references,
and remove the local branch. Retain release tags and avoid rewriting shared history.

## Solo-Maintainer Notes

Pull requests remain useful without a second maintainer because they run checks against the proposed
merge and keep GitHub as the authoritative integration surface. Required human approvals may remain
disabled until another reviewer is consistently available. Keep any administrator bypass narrow,
intentional, and documented in the branch-protection policy.

## Keep Private Elsewhere

Keep credentials, PyPI recovery codes, AWS account identifiers, emergency bypass procedures, private
incident details, and embargoed vulnerability reports outside the repository. Public runbooks should
explain policy and reproducible workflows without exposing privileged operational details.
