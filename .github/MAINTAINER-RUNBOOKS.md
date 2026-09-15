# Maintainer Runbooks

These public runbooks describe routine work with protected branches, pull requests, releases, and
post-merge automation. They are intentionally independent of programming language and build system.
Repository-specific branch names, checks, and publication behavior are identified explicitly.

- [Operating Model](#operating-model)
- [Before Starting Branch Work](#before-starting-branch-work)
- [Feature and Bugfix Work](#feature-and-bugfix-work)
- [Release Work](#release-work)
- [Hotfix Work](#hotfix-work)
- [Support Branch Work](#support-branch-work)
- [Synchronizing the Default Branch Back to Development](#synchronizing-the-default-branch-back-to-development)
- [Tagging](#tagging)
- [Post-Merge Deployment or Publication](#post-merge-deployment-or-publication)
- [Handling Failed Checks](#handling-failed-checks)
- [Reverting or Recovering a Change](#reverting-or-recovering-a-change)
- [Cleaning Up Branches](#cleaning-up-branches)
- [Solo-Maintainer Notes](#solo-maintainer-notes)
- [Keep Private Elsewhere](#keep-private-elsewhere)
- [References](#references)

## Operating Model

The general operating model is:

- Work happens on short-lived topic branches.
- Authoritative integration happens through hosted pull requests.
- Required checks validate the proposed integration before a protected branch changes.
- The hosted repository, not a maintainer's local clone, is authoritative for protected branches.
- Post-merge deployment and publication jobs complement pre-merge validation; they do not replace it.

This repository uses GitFlow-style branch roles:

- `feature/*` and `bugfix/*` branches start from and target `develop`.
- `chore/*`, `ci/*`, `docs/*`, and `dependabot/*` branches target `develop`.
- `sync/*` branches reconcile `main` back into `develop`.
- `release/*` branches start from `develop` and target `main`.
- `hotfix/*` branches start from and target `main`.
- `support/*` branches are exceptional and require an agreed base, integration strategy, and
  corresponding update to the pull-request target guard before use.
- `develop` and `main` are protected integration branches.

Git Flow tooling is optional. The examples in this document assume a compatible implementation, but
ordinary Git commands may create and publish the same branches. Confirm which Git Flow
implementation is installed before relying on implementation-specific commands or options.

Do not use local Git Flow `finish` commands, such as `git flow feature finish`, `git flow release
finish`, or `git flow hotfix finish`, as the authoritative integration or cleanup step. They
typically perform local merges and branch deletion. Merge through the hosted pull request, then
clean up the local working branch explicitly.

See [BRANCH-PROTECTION.md] for enforcement settings and [CONTRIBUTING.md] for contributor-facing
expectations.

## Before Starting Branch Work

1. Confirm the intended change, target branch, and related issue or operational objective.
2. Check that the working tree contains no unrelated changes. Preserve or commit existing work before
   switching branches.
3. Fetch and prune remote references:

   ```bash
   git fetch --prune origin
   ```

4. Confirm the chosen base matches its remote branch. Update a clean local integration branch with a
   fast-forward-only pull when needed. Replace `BASE_BRANCH` with the intended branch name:

   ```bash
   git switch BASE_BRANCH
   git pull --ff-only origin BASE_BRANCH
   ```

5. Create a focused topic branch using the repository's naming convention.
6. Install development dependencies and hooks, then run `make check`.
7. Do not create commits directly on a protected integration branch.

## Feature and Bugfix Work

Use `feature/*` for enhancements, `bugfix/*` for non-emergency corrections, and the documented
maintenance prefixes for focused non-feature work entering through `develop`.

1. Start from current `develop`.
2. Create the working branch. For example:

   ```bash
   git flow feature start my-change
   ```

   If the installed Git Flow implementation does not support the desired branch type, use ordinary
   Git instead:

   ```bash
   git switch -c bugfix/my-change develop
   ```

3. Implement one cohesive change with tests and documentation where applicable.
4. Update `CHANGELOG.md` for user-visible behavior.
5. Run `make check`, then push the branch using its full name:

   ```bash
   git push -u origin BRANCH_NAME
   ```

6. Open a pull request targeting `develop`.
7. Confirm the required `Guard pull request target`, `Validate pull request`, dependency-matrix, and
   distribution checks pass.
8. Merge through GitHub using the configured merge method or merge queue.
9. Confirm the authoritative merge, then follow [Cleaning Up Branches](#cleaning-up-branches).

## Release Work

Use `release/*` to stabilize and promote a planned release from `develop` to `main`. Follow the
public [release checklist] and [release policy] together with these repository-specific steps.

1. Confirm `develop` contains the intended release scope and its required checks are passing.
2. Choose the next semantic version under the release policy.
3. Create `release/<version>` from current `develop`.
4. Limit changes to release preparation, stabilization, documentation, and necessary corrections.
5. Move completed `Unreleased` entries into a dated `## <version> - YYYY-MM-DD` section in
   `CHANGELOG.md`. Do not edit a package version; `setuptools-scm` derives it from Git tags.
6. Prepare `docs/releases/v<version>.md` using the [release notes template].
7. Run `make release-changelog RELEASE_VERSION=<version>` and `make check-ci-local`.
8. Build the sdist and wheel, run `twine check`, and install each distribution into a separate clean
   environment for preliminary import and synthesis checks.
9. Push the branch and open a pull request targeting `main`.
10. Confirm required checks and review requirements pass, then merge through GitHub.
11. Fetch the authoritative merged `main` commit and create the release tag as described in
    [Tagging](#tagging).
12. Complete [Post-Merge Deployment or Publication](#post-merge-deployment-or-publication) checks.
13. Synchronize `main` back into `develop`.

The repository does not yet publish to PyPI. Do not upload a package manually or configure external
release credentials until trusted publishing has been reviewed and explicitly enabled.

## Hotfix Work

Use `hotfix/*` for urgent corrections that must reach the released branch before the normal release
cycle.

1. Confirm the issue warrants bypassing the normal `develop`-first path and identify the affected
   release or behavior.
2. Start from current `main` and create `hotfix/<version>`.
3. Make the smallest safe change and add regression coverage when practical.
4. Run focused validation plus the normal required quality gates.
5. Document urgency, compatibility, validation, rollback, and the planned sync to `develop`.
6. Push the branch and open a pull request targeting `main`.
7. Confirm required checks and review requirements pass, then merge through GitHub.
8. Tag the merged commit only when it represents a corresponding versioned release.
9. Verify post-merge automation and synchronize `main` back into `develop`.

Urgency does not by itself justify force pushing, skipping required checks, exposing credentials, or
silently bypassing branch protection.

## Support Branch Work

Use `support/*` only to maintain an older release line that cannot safely receive changes from the
current `main` or `develop` history.

Before creating a support branch, document:

- The release line and base commit or tag being supported.
- The expected lifetime and support owner.
- The allowed change scope.
- The pull request target and validation requirements.
- How applicable fixes will propagate to current release and development branches.

Do not assume `main` or `develop` is the correct pull request target for a support branch. Agree on
the integration strategy first, update the pull-request target guard through the ordinary reviewed
workflow, and protect long-lived support branches consistently with their risk.

## Synchronizing the Default Branch Back to Development

After a release, hotfix, revert, or other authorized change reaches `main`, synchronize it back into
`develop` deliberately.

1. Fetch current `origin/main` and `origin/develop`.
2. Create `sync/main-into-develop` from `origin/develop`.
3. Merge `origin/main` into the sync branch.
4. Resolve conflicts there and run relevant validation.
5. Push the sync branch and open a pull request targeting `develop`.
6. Confirm required checks pass, then merge through GitHub or its merge queue.
7. Clean up the sync branch after confirming the merge.

Do not assume a local Git Flow `finish` command already synchronized both protected branches.

## Tagging

Tag only when the project intentionally publishes a versioned release.

- Tag the authoritative merged `main` commit.
- Use `vMAJOR.MINOR.PATCH` under the repository's versioning policy.
- Create an annotated tag; require signed tags only when signing is an established project policy.
- Verify the target commit, changelog section, and release document before pushing the tag.
- Never move or reuse a published release tag. Correct a mistake with a new version.
- Confirm the tag-triggered release workflow is expected to run before pushing.

Example for release `1.2.0`, after replacing `MAIN_COMMIT_SHA` with the verified commit:

```bash
git tag -a v1.2.0 MAIN_COMMIT_SHA -m "Release 1.2.0"
git push origin v1.2.0
```

## Post-Merge Deployment or Publication

For projects with deployment or publication automation:

1. Confirm the expected workflow started from the authoritative merged commit or immutable tag.
2. Wait for protected environments and deployment or publication jobs to finish.
3. Review emitted outputs, artifacts, and smoke-test results.
4. Verify the externally visible behavior appropriate to the change.
5. Record or link the workflow run in release or incident notes when operationally significant.

In this repository, pushing an annotated semantic-version tag runs `.github/workflows/cd.yml`. It
builds the source distribution and wheel from the tag, validates and smoke-tests them, creates
checksums and a CycloneDX SBOM, and publishes those assets to the corresponding GitHub Release. It
does not publish to PyPI or deploy AWS resources.

For historical recovery, manually dispatch the workflow with an existing immutable annotated tag.
The workflow does not create, move, or reuse tags, and a backfilled release is not marked latest.

## Handling Failed Checks

1. Identify the first meaningful failure in the required job rather than relying only on the final
   workflow status.
2. Reproduce the failure locally when practical.
3. Fix the cause on the same topic branch and add or improve regression coverage when appropriate.
4. Push the correction and let hosted checks rerun on the new commit.
5. Rerun an unchanged job only when evidence indicates a transient service or runner failure.
6. Do not weaken or bypass a required check merely to merge the current pull request.

If a merge-group check fails, inspect the combined merge-group result. Update the topic branch or
resolve its interaction with queued changes before returning it to the queue.

## Reverting or Recovering a Change

Prefer a new pull request that reverts the merged change. Do not rewrite protected history with
`reset`, a force push, or a moved release tag.

1. Identify the exact merged pull request or commit and assess compatibility, artifact,
   infrastructure, and security impact.
2. Choose between a forward fix and a revert based on which path restores safe behavior sooner.
3. Create a revert or hotfix branch from the affected protected branch.
4. Validate the recovery change and open a pull request through the normal protected path.
5. After merge, verify publication recovery when applicable.
6. Synchronize recovery applied to `main` back into `develop` and other affected release lines.
7. Record the cause and follow-up work without placing sensitive incident details in the repository.

If a package is eventually published to PyPI, follow PyPI's release and yanking semantics and
document the consumer impact. Use a documented emergency bypass only when waiting for the normal
protected flow creates greater harm; preserve an audit trail and follow immediately with review,
validation, synchronization, and removal of any temporary bypass.

## Cleaning Up Branches

Clean up only after confirming the hosted pull request merged successfully and no other open work
depends on the branch.

1. Switch away from the working branch.
2. Fetch and prune remote references.
3. Confirm the protected target contains the intended change.
4. Delete the local branch with the non-forcing form:

   ```bash
   git branch -d BRANCH_NAME
   ```

5. Delete the remote branch through the pull request interface or explicitly when no longer needed.

Avoid `git branch -D` unless the unmerged commits have been reviewed and their loss is intentional.
Retain release tags and never rewrite shared history during cleanup.

## Solo-Maintainer Notes

Pull requests remain useful without another human reviewer because they preserve review context,
exercise required checks, and keep protected-branch integration auditable.

A solo maintainer cannot satisfy a mandatory approval by approving their own pull request. Configure
zero required approvals while retaining pull requests, required checks, and conversation resolution;
alternatively, document a narrowly scoped bypass policy. Increase the approval requirement when an
independent reviewer is routinely available.

Do not normalize broad administrator bypass merely because the project currently has one maintainer.

## Keep Private Elsewhere

This public file should describe policy and ordinary procedures. Store sensitive operational details
in an approved private system, including:

- Credentials, secret locations, and credential-recovery procedures.
- Exact emergency bypass credentials or access paths.
- Security-incident investigation and containment details.
- Account recovery, ownership transfer, or succession information.
- Customer, production, personal, or other confidential data.

Public documentation may identify that a private procedure exists and who is responsible for it,
without disclosing the sensitive procedure itself.

## References

- [Branch protection policy][BRANCH-PROTECTION.md]
- [Contributor workflow][CONTRIBUTING.md]
- [Release checklist]
- [Release policy]
- [Release notes template]
- [Git Flow AVH command reference][git-flow-avh]
- [GitHub merge queue guidance][merge-queue]
- [GitHub pull request reverts][revert-pr]

[BRANCH-PROTECTION.md]: BRANCH-PROTECTION.md
[CONTRIBUTING.md]: ../CONTRIBUTING.md
[git-flow-avh]: https://github.com/petervanderdoes/gitflow-avh#git-flow-usage
[merge-queue]: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue
[release checklist]: ../RELEASE-CHECKLIST.md
[release notes template]: RELEASE-NOTES-TEMPLATE.md
[release policy]: ../RELEASE-POLICY.md
[revert-pr]: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/reverting-a-pull-request
