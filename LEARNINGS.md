# Learnings

This file captures reusable lessons supported by implementation, test, or workflow evidence. Each
entry uses `Symptom → Cause → Fix → Verification`.

- [CloudFront Certificate Creation Fails or Is Rejected](#cloudfront-certificate-creation-fails-or-is-rejected)
- [Static Content Changes Are Not Visible When Expected](#static-content-changes-are-not-visible-when-expected)
- [An S3 Bucket Remains After Stack Deletion](#an-s3-bucket-remains-after-stack-deletion)
- [A CDK Refactor Plans Unexpected Resource Replacement](#a-cdk-refactor-plans-unexpected-resource-replacement)
- [Local Pytest Does Not Run Every Repository Test](#local-pytest-does-not-run-every-repository-test)
- [Lowest-Dependency CI Drifts from Package Metadata](#lowest-dependency-ci-drifts-from-package-metadata)
- [A GitHub Actions Pin Check Fails](#a-github-actions-pin-check-fails)
- [A Release Build Has the Wrong Version](#a-release-build-has-the-wrong-version)
- [Disposable Deployment Cleanup Needs Operator Follow-Up](#disposable-deployment-cleanup-needs-operator-follow-up)
- [Documentation and Automation Claims Drift Apart](#documentation-and-automation-claims-drift-apart)

## CloudFront Certificate Creation Fails or Is Rejected

**Symptom:** A custom-domain configuration cannot create its certificate, or synthesis raises a
region error.

**Cause:** CloudFront certificates must be in `us-east-1`. Construct-managed certificate creation
also needs a concrete stack region; an environment-agnostic stack yields an unresolved token.

**Fix:** Deploy the consuming stack explicitly in `us-east-1`, or create/import a certificate in
`us-east-1` and pass it through `certificate` while managing DNS as appropriate.

**Verification:** Synthesize the Route 53-managed or external-DNS example and run the certificate
region and property-validation unit tests.

## Static Content Changes Are Not Visible When Expected

**Symptom:** A browser keeps serving an old stable-named asset after deployment.

**Cause:** The path was classified as immutable even though its URL does not change with its bytes.
The deployment gives matching paths long-lived `immutable` browser metadata.

**Fix:** Reserve `immutable_asset_paths` for content-addressed filenames. Leave HTML, favicons, and
stable JavaScript or CSS names in the mutable deployment, or fingerprint them.

**Verification:** Inspect synthesized bucket deployments for the expected `cache-control` metadata
and invalidation paths, then run `make test-unit test-examples`.

## An S3 Bucket Remains After Stack Deletion

**Symptom:** Deleting a consumer stack leaves the content or access-log bucket behind.

**Cause:** Retention is intentional. The content bucket defaults to `RemovalPolicy.RETAIN`, the log
bucket is always retained, and automatic object deletion is disabled. A versioned, non-empty bucket
also cannot be removed merely by changing its removal policy.

**Fix:** Treat retained buckets as separately managed state. If a disposable consumer selects
deletion, give it a reviewed emptying strategy; do not broadly delete buckets as a shortcut. Review
the related storage and retention [cost considerations].

**Verification:** Review synthesized `DeletionPolicy` and `UpdateReplacePolicy` values and confirm
the intended bucket and object lifecycle before deployment.

## A CDK Refactor Plans Unexpected Resource Replacement

**Symptom:** `cdk diff` shows replacement of a bucket or another resource after a source refactor.

**Cause:** Moving a construct in the tree or changing its construct ID changes its logical ID even
when resource properties are equivalent.

**Fix:** Preserve construct paths and IDs. If replacement is intentional, document the migration and
data-lifecycle consequences; otherwise use CDK-supported refactoring techniques. Follow the
[construct-adoption playbook] for state-preserving consumer migrations.

**Verification:** Compare synthesized templates, run stateful-resource identity regression tests,
and inspect `cdk diff` before deployment.

## Local Pytest Does Not Run Every Repository Test

**Symptom:** `python -m pytest` passes, but distribution, installation, or security checks did not
run.

**Cause:** Default discovery includes only `tests/unit` and `tests/integration` so the fast suite
stays deterministic and credential-free. End-to-end and meta suites are explicit.

**Fix:** Use `make test-distribution`, `make test-installation`, `make test-security`, or `make
test-full`. Use `make check-ci-local` for the broad local CI gate.

**Verification:** Confirm output includes the intended `tests/e2e` or `tests/meta` module.

## Lowest-Dependency CI Drifts from Package Metadata

**Symptom:** The dependency-boundary policy check fails after editing runtime requirements.

**Cause:** `requirements/lowest.txt` no longer matches minimum direct versions in `pyproject.toml`.

**Fix:** Update lowest constraints with canonical package metadata; do not turn the file into an
application lockfile. The newest boundary remains dynamically resolved within allowed ranges.

**Verification:** Run `make dependency-policy`, then test lowest and newest configurations in
separate clean environments as documented in the [testing guide].

## A GitHub Actions Pin Check Fails

**Symptom:** CI or pre-commit rejects a workflow even though an action reference is valid.

**Cause:** Remote actions must use immutable full commit SHAs; floating tags violate repository
supply-chain policy.

**Fix:** Resolve the intended release to its reviewed commit SHA, use it in `uses:`, and retain a
human-readable pinned-version comment.

**Verification:** Run `make github-actions-pins` and review job-scoped permissions.

## A Release Build Has the Wrong Version

**Symptom:** A wheel or sdist reports a development or fallback version instead of the release.

**Cause:** Versions come from Git metadata through `setuptools-scm`; shallow, untagged, dirty, or
incorrectly tagged source cannot reproduce the release version.

**Fix:** Build authoritative artifacts from the existing annotated `vMAJOR.MINOR.PATCH` tag with
complete Git history. Do not add a source version constant or move a released tag.

**Verification:** Inspect artifact metadata, run distribution and clean-installation tests, and
confirm the [release playbook] validates the matching dated changelog section.

## Disposable Deployment Cleanup Needs Operator Follow-Up

**Symptom:** The manual deployment-test job is interrupted before cleanup completes.

**Cause:** Cleanup runs in an `always()` step, but a cancelled runner or timeout can prevent the
wait from finishing.

**Fix:** Inspect CloudFormation for the exact `AwsCdkStaticSiteTest-<run-id>` stack and delete only
that stack through a reviewed operator path. Never use a broad name pattern.

**Verification:** Wait for `stack-delete-complete` and confirm the exact stack no longer exists, as
described in the [disposable deployment runbook].

## Documentation and Automation Claims Drift Apart

**Symptom:** A guide names a command, workflow job, required check, supported version, or public
property that no longer exists or behaves differently.

**Cause:** Prose was updated independently from the executable source that defines the contract, or
a broad documentation copy reused assumptions from another repository.

**Fix:** Trace the claim to its canonical source: `pyproject.toml` for package/tool policy,
`Makefile` for contributor commands, workflow YAML for triggers and job names, implementation and
tests for construct behavior, and tags plus release automation for publication. Update every owned
mirror in the same focused change using the [documentation synchronization guide].

**Verification:** Run the applicable executable check, `make docs-strict` for Sphinx content, and a
relative-link/structure check for standalone Markdown. Review the final diff for unsupported future
state, private identifiers, and stale copied names.

[construct-adoption playbook]: docs/playbooks/adopt-static-site-construct.md
[cost considerations]: docs/COSTS.md
[disposable deployment runbook]: docs/runbooks/disposable-aws-deployment.md
[documentation synchronization guide]: docs/development/documentation-sync.md
[release playbook]: docs/playbooks/release.md
[testing guide]: docs/TESTING.md
