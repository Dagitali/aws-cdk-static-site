# Repository Incident Response

This public runbook covers CI, release, package-artifact, documentation-publication, and disposable
AWS deployment-test incidents. Keep private contacts, credentials, account identifiers, and
vulnerability details in approved private systems. Use `SECURITY.md` for vulnerability reporting.

- [Triage](#triage)
- [Contain and Recover](#contain-and-recover)
- [Verify and Close](#verify-and-close)

## Triage

1. Identify the exact workflow run, commit or immutable tag, artifact, environment, and first
   meaningful failure.
2. Classify impact: validation-only, incorrect release assets, consumer-facing package behavior,
   credential exposure, or unexpected AWS resources.
3. Preserve logs and metadata without copying secrets into issues or tracked files.
4. Pause further publication or cloud mutation through the narrowest existing control when needed;
   do not rewrite Git history or move a published tag.
5. Escalate suspected credential or vulnerability exposure through private channels immediately.

## Contain and Recover

- **CI failure:** reproduce locally, fix on the same topic branch, and rerun unchanged jobs only
  when evidence shows a transient failure. Do not weaken a required check.
- **Bad merged change:** prefer a reviewed forward fix or revert. Synchronize recovery from `main`
  back to `develop` and affected release lines.
- **Incorrect release:** retain the immutable tag and release evidence. Correct with a new version;
  do not replace assets silently when consumers may have downloaded them.
- **Failed historical backfill:** use only the documented manual dispatch with an existing annotated
  tag. Verify the run does not become the latest release.
- **Disposable AWS test:** identify the exact `AwsCdkStaticSiteTest-<run-id>` stack. Follow the
  cleanup procedure in the [deployment runbook]; never delete by a broad prefix.
- **Suspected credential exposure:** stop using the credential, follow the provider's private
  rotation/revocation process, and review workflow permissions and logs before resuming automation.

Any external rerun, deletion, revocation, publication, or repository-settings change requires the
appropriate maintainer authorization.

## Verify and Close

Confirm required checks, artifact metadata and checksums, release visibility, or exact stack
deletion as applicable. Record a concise timeline, cause, impact, recovery, and prevention without
sensitive detail. Add a regression test or policy check when possible, update a runbook for changed
operations, and add a `Symptom → Cause → Fix → Verification` entry to `LEARNINGS.md` when the lesson
is reusable.

[deployment runbook]: disposable-aws-deployment.md
