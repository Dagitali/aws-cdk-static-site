# Update Required Checks

Use this runbook when a GitHub Actions job name, workflow trigger, supported-version matrix, merge
queue configuration, or reliability decision changes the checks required on protected branches. The
authoritative desired configuration remains [Branch Protection]; this runbook describes how to apply
and verify it safely.

- [Triggers](#triggers)
- [Prerequisites](#prerequisites)
- [Safety Boundaries](#safety-boundaries)
- [Plan the Transition](#plan-the-transition)
- [Observe the Emitted Checks](#observe-the-emitted-checks)
- [Update the Hosted Rules](#update-the-hosted-rules)
- [Verify Enforcement](#verify-enforcement)
- [Troubleshoot Pending or Missing Checks](#troubleshoot-pending-or-missing-checks)
- [Rollback](#rollback)
- [Record the Change](#record-the-change)

## Triggers

Run this procedure when:

- A required workflow or job is added, removed, or renamed;
- A matrix dimension changes the expanded job names;
- A workflow gains or loses `pull_request` or `merge_group` coverage;
- A required job gains path filters, job conditions, or dependencies;
- An advisory check is promoted to required or a required check is demoted;
- Merge queue is enabled, disabled, or reconfigured; or
- The protected branch set or GitFlow routing changes.

Step names do not trigger a required-check update because GitHub branch protection selects emitted
job checks, not workflow steps.

## Prerequisites

- Repository administration permission or an approved operator who can change rulesets.
- A focused topic branch and representative pull request targeting the affected protected branch.
- Successful hosted runs that expose the exact current check names and their GitHub Actions source.
- The current [Branch Protection] configuration and [CI/CD workflow map].
- A record of the existing ruleset settings and bypass actors before editing.

Do not store tokens, account recovery data, or screenshots containing private repository information
in this public repository.

## Safety Boundaries

- Do not remove pull-request, conversation-resolution, force-push, or deletion protections while
  changing check names.
- Require only jobs that run for every applicable pull request and, when enabled, every merge group.
- Do not require deployment, publication, manual, scheduled, or push-only jobs.
- Do not require path-filtered jobs unless a reliable companion reports the same required result for
  excluded paths.
- Keep required job names unique across workflows.
- Select the exact emitted job name, including expanded matrix values; never select a step name or
  copy an unexpanded matrix expression.
- Keep bypass access empty or narrowly scoped and documented.
- Update `develop` first when both protected branches share a policy, then apply the proven
  configuration to `main`.

## Plan the Transition

1. Compare the workflow change with the current required and advisory lists in [Branch Protection].
2. Confirm that the new or renamed job runs on `pull_request` for every protected target.
3. If merge queue is enabled, confirm the workflow handles `merge_group` and emits the same job.
4. Check path filters, job-level `if` expressions, matrix exclusions, dependencies, and concurrency
   settings that could prevent the result from appearing.
5. Decide whether the change can be staged without a protection gap.

For a required-job rename, prefer this compatibility sequence:

1. Add the new emitted check while temporarily retaining the old required check result.
2. Run both on a representative pull request.
3. Add the new check to the ruleset while the old check remains required.
4. Merge the workflow transition.
5. Remove the old required check only after the new check succeeds on protected-branch pull requests
   and merge groups.
6. Remove temporary compatibility automation in a follow-up change.

If retaining both results is impractical, document the narrow transition window and coordinate the
workflow merge with the hosted ruleset edit. Do not use a broad or permanent bypass to solve a name
transition.

## Observe the Emitted Checks

1. Open or update the representative pull request.
2. Wait for every relevant workflow to finish.
3. Inspect the pull request's checks and record the exact successful job names.
4. Confirm each result is associated with GitHub Actions when source restriction is available.
5. Repeat with a merge-group entry when merge queue is enabled.
6. Confirm matrix jobs emit every supported Python and dependency-boundary combination documented in
   [Branch Protection].
7. Confirm advisory jobs remain visible but are not accidentally selected as required.

Do not infer emitted names solely from workflow YAML. Matrix expansion and display-name expressions
can change the names GitHub exposes to branch protection.

## Update the Hosted Rules

1. Open the active repository ruleset under **Settings**, **Rules**, and **Rulesets**. If rulesets
   are unavailable, open the equivalent branch protection rule under **Settings** and **Branches**.
2. Confirm the rule targets the intended branch before editing.
3. Preserve the existing pull-request, review, conversation, deletion, force-push, and bypass
   settings.
4. Add the newly verified check names.
5. Keep old check names during a staged transition.
6. Select GitHub Actions as the expected source when supported.
7. Save the rule and confirm it remains active.
8. Repeat for each protected branch that intentionally shares the policy.
9. After the transition succeeds, remove stale check names and save again.

Apply changes to `develop` and validate them before applying the same set to `main`, unless the
repository's branch model requires a different reviewed sequence.

## Verify Enforcement

Use a fresh or rerun representative pull request to confirm:

- Every documented required check is reported and must pass;
- An intentionally failing required check blocks merging;
- Advisory check failure does not block merging;
- No required check remains permanently expected or pending;
- Direct updates, force pushes, and deletion remain blocked;
- Review and conversation-resolution requirements remain intact; and
- Merge queue accepts the pull request and runs the same required checks when enabled.

Compare the active hosted settings with [Branch Protection] after verification. The document and
hosted controls must describe the same required and advisory sets.

## Troubleshoot Pending or Missing Checks

When GitHub reports an expected check indefinitely:

1. Confirm the selected name exactly matches a check emitted by the latest representative run.
2. Confirm the workflow ran for the pull request's target branch and event.
3. Check path filters, job conditions, matrix exclusions, skipped dependencies, and concurrency
   cancellation.
4. Confirm the required name refers to a job rather than a step.
5. Check for duplicate job names across workflows.
6. For merge queue, confirm the workflow handles `merge_group`.
7. Remove a stale required name only after its verified replacement is enforcing the intended gate.

Do not work around a pending check with a routine administrator bypass.

## Rollback

If the new configuration blocks valid pull requests or fails to enforce the intended gate:

1. Restore the last known-good required-check set from the pre-change record.
2. Restore the compatible workflow job name or trigger if the hosted rule cannot be corrected first.
3. Verify enforcement on a representative pull request.
4. Revert temporary bypass access immediately if one was explicitly approved for recovery.
5. Replan the transition with an overlapping old and new result.

Rollback must preserve pull-request and history protections.

## Record the Change

- Update the required and advisory lists in [Branch Protection].
- Update the [CI/CD workflow map] when workflow responsibilities or triggers changed.
- Record the validation pull request and date in the private operator record when appropriate.
- Keep workflow actions pinned to full commit SHAs.
- Confirm the repository's documented branch roles and actual target guards still agree.

[Branch Protection]: ../../.github/BRANCH-PROTECTION.md
[CI/CD workflow map]: ../../CI-CD-WORKFLOWS.md
