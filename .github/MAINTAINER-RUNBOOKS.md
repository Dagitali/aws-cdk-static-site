# Maintainer Runbooks

- [Start Repository Work](#start-repository-work)
- [Develop a Feature Or Bug Fix](#develop-a-feature-or-bug-fix)
- [Prepare a Release](#prepare-a-release)
- [Apply a Hotfix](#apply-a-hotfix)
- [Investigate Failed Checks](#investigate-failed-checks)
- [Recover a Release](#recover-a-release)
- [Clean Up](#clean-up)

## Start Repository Work

1. Confirm the intended change and target branch.
2. Preserve unrelated working-tree changes.
3. Fetch remote references and update the appropriate protected base with a fast-forward-only pull.
4. Create a focused branch using the documented GitFlow branch families in
   `.github/BRANCH-PROTECTION.md`.
5. Install development dependencies and hooks, then run `make check`.

Do not use local Git Flow `finish` commands as the authoritative integration step. Merge through a
GitHub pull request and clean up branches afterward.

## Develop a Feature Or Bug Fix

1. Start from current `develop`.
2. Implement one cohesive change with tests and documentation.
3. Update `CHANGELOG.md` for user-visible behavior.
4. Run `make check` and push the topic branch.
5. Open a pull request targeting `develop` and complete required checks.

## Prepare a Release

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

Keep credentials, PyPI recovery codes, AWS account identifiers, private incident details, and
embargoed vulnerability reports outside the repository.
