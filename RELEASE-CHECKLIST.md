# Release Checklist

Use this public checklist for release readiness. Keep credentials, recovery codes, private account
details, and incident procedures outside the repository.

- [Prepare](#prepare)
- [Validate](#validate)
- [Integrate and Tag](#integrate-and-tag)
- [Publish](#publish)
- [Close Out](#close-out)

## Prepare

- [ ] Confirm the intended version and compatibility impact under the
      [release policy].
- [ ] Create `release/<version>` from current `develop`.
- [ ] Finalize user-facing changes, tests, documentation, and `CHANGELOG.md`.
- [ ] Confirm package metadata, supported Python versions, dependencies, and public exports.
- [ ] Draft release notes from `.github/RELEASE-NOTES-TEMPLATE.md`.

## Validate

- [ ] Run `make check` from a clean development environment.
- [ ] Build source and wheel distributions with `make dist`.
- [ ] Inspect archive contents and confirm `twine check` succeeds.
- [ ] Install the wheel in a clean environment and smoke-test imports and CDK synthesis.
- [ ] Review synthesized changes for security, replacement risk, and cost implications.
- [ ] Confirm required GitHub Actions are pinned and pass on the release pull request.

## Integrate and Tag

- [ ] Open a pull request from `release/<version>` to protected `main`.
- [ ] Merge through GitHub after required checks and reviews pass.
- [ ] Fetch the authoritative merged `main` commit.
- [ ] Create an annotated `v<version>` tag on that exact commit.
- [ ] Push the tag without moving or reusing an existing released version.

## Publish

- [ ] Build authoritative artifacts from the tag rather than an untagged working tree.
- [ ] Verify the derived package version matches the tag.
- [ ] Publish the GitHub Release and attach artifacts when the release process supports it.
- [ ] Publish to PyPI only through an approved trusted-publishing workflow.

The final two publication items remain intentionally inactive until release automation is reviewed
and enabled.

## Close Out

- [ ] Confirm release notes, artifacts, and checks are visible and correct.
- [ ] Synchronize `main` back into `develop` through a `sync/*` pull request.
- [ ] Delete merged working branches and prune obsolete remote references.
- [ ] Record follow-up work without rewriting the released tag or shared history.

[release policy]: RELEASE-POLICY.md
