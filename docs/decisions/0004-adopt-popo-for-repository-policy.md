# 0004: Adopt Popo for Repository-Policy Checks

Status: Accepted

- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)
- [Alternatives Considered](#alternatives-considered)
- [Verification](#verification)
- [References](#references)

## Context

The repository contains local implementations and direct tests for Markdown links, GitHub Actions
pins, dependency boundaries, Python-version policy, and release changelog validation. Popo was
extracted to provide these read-only checks consistently across repositories. Maintaining both
implementations would duplicate fixes and allow their behavior to drift.

## Decision

Use Popo as the authoritative implementation behind the existing Make targets, pre-commit hooks,
continuous integration, and tagged-release validation. Pin the reviewed Popo `v0.2.2` commit as a
development dependency and declare this repository's policy explicitly under `[tool.popo]` in
`pyproject.toml`.

Retain `scripts/` and its direct tests temporarily as a deprecated compatibility surface. Do not add
new policy behavior there. Remove the package and those tests in a follow-up after Popo-backed local
and hosted gates have completed a migration window and all remaining callers have been rechecked.

## Consequences

Policy fixes and enhancements now belong in Popo, while this repository owns only its policy
configuration and integration contracts. Contributor setup requires Git access to the pinned Popo
revision until the tool is published to a package index. Existing Make target names remain stable.
The construct's runtime dependencies, public API, synthesized infrastructure, and AWS permissions do
not change.

## Alternatives Considered

Continuing to maintain the local implementation preserves a self-contained checkout but duplicates
the extracted tool and its regression suite. Removing `scripts/` immediately reduces duplication
sooner but discards an established compatibility path before local and hosted callers have exercised
the replacement.

## Verification

Run each Popo-backed Make target, the focused Make contract tests, the default test suites, and the
repository documentation and workflow-pin checks. Confirm the tagged-release workflow installs the
same pinned revision before invoking the release-changelog command.

## References

- [Popo repository](https://github.com/Dagitali/popo)
- [Testing guide](../TESTING.md)
- [Contributor guide](../../CONTRIBUTING.md)
- [CI/CD workflow map](../../CI-CD-WORKFLOWS.md)
