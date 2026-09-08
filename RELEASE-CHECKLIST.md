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
- [ ] Move completed `Unreleased` entries into a dated `## <version> - YYYY-MM-DD`
      changelog section before tagging.
- [ ] Confirm package metadata, supported Python versions, dependencies, and public exports.
- [ ] Draft release notes from `.github/RELEASE-NOTES-TEMPLATE.md`.

## Validate

- [ ] Run `make check` from a clean development environment.
- [ ] Build the sdist and wheel with `make dist`.
- [ ] Inspect archive contents and confirm `twine check` succeeds.
- [ ] Install each distribution in a separate clean environment and smoke-test imports and the
      package's representative example.
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
- [ ] Confirm the tag-triggered workflow publishes the GitHub Release with its sdist, wheel,
      checksums, and SBOM.
- [ ] Publish to PyPI only through an approved trusted-publishing workflow.

PyPI publication remains intentionally inactive until trusted publishing is reviewed and enabled.

## Close Out

- [ ] Confirm release notes, artifacts, and checks are visible and correct.
- [ ] Synchronize `main` back into `develop` through a `sync/*` pull request.
- [ ] Delete merged working branches and prune obsolete remote references.
- [ ] Record follow-up work without rewriting the released tag or shared history.

[release policy]: RELEASE-POLICY.md
