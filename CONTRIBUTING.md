# Contributing Guidelines

Contributions to source code, tests, documentation, and repository automation are welcome through
GitHub issues and pull requests. By submitting a contribution, you agree that it may be distributed
under this project's [MIT License](LICENSE).

- [Ways to Contribute](#ways-to-contribute)
- [Development Workflow](#development-workflow)
- [Protected-Branch GitFlow](#protected-branch-gitflow)
- [Local Quality Gates](#local-quality-gates)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community Standards](#community-standards)

## Ways to Contribute

Useful contributions include:

- reproducible bug reports with version and environment details;
- focused feature proposals that explain the underlying need;
- tests for public behavior and compatibility contracts;
- documentation corrections, examples, and accessibility improvements; and
- code, packaging, security, or automation improvements.

Discuss substantial changes in an issue before investing in an implementation. Do not include
credentials, private data, or vulnerability details in public issues.

## Development Workflow

1. Create a focused topic branch from the appropriate protected base.
2. Install the development dependencies and Git hooks with `make hooks`.
3. Implement one cohesive change, including tests and documentation when applicable.
4. Run `make check` and address failures rather than weakening the checks.
5. Update `CHANGELOG.md` for user-visible behavior.
6. Push the branch and open a pull request using the repository template.
7. Merge through GitHub after the required checks and reviews pass.

Package versions are derived from Git tags by `setuptools-scm`; do not add or hand-edit a second
version source. See [RELEASE-POLICY.md](RELEASE-POLICY.md) and
[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) for release-affecting changes.

## Protected-Branch GitFlow

This repository uses GitFlow-style branch roles with GitHub-protected integration branches:

- `feature/*`, `bugfix/*`, and routine maintenance branches target `develop`;
- `release/*` and `hotfix/*` target `main`; and
- `sync/*` carries released changes from `main` back to `develop`.

Do not treat `git flow ... finish` as the authoritative integration step: it performs local merges
that bypass the pull-request review surface. The complete branch map and required checks are in
[.github/BRANCH-PROTECTION.md](.github/BRANCH-PROTECTION.md), and maintainer procedures are in
[.github/MAINTAINER-RUNBOOKS.md](.github/MAINTAINER-RUNBOOKS.md).

## Local Quality Gates

Run the complete local gate with:

```bash
make check
```

Useful focused targets include:

```bash
make fmt
make lint
make typecheck
make test
make dist
make workflow-pins
make python-policy
```

Install the staged Git hooks with `make hooks`. Ruff is the canonical formatter and linter, mypy is
the type-checking gate, and settings shared by supported Python tools are centralized in
`pyproject.toml`.

## Testing

Add tests for observable behavior and validation failures. Prefer stable public properties over
generated implementation details such as CDK logical IDs unless an identifier is itself part of a
compatibility contract. Unit tests must not require AWS credentials or network access.

See [docs/TESTING.md](docs/TESTING.md) and [tests/README.md](tests/README.md) for test organization,
markers, and commands.

## Documentation

Keep prose concise, use descriptive link text, and wrap code, file names, commands, and identifiers
in backticks. Update nearby examples and cross-references when behavior or public interfaces change.
Prefer repository-relative links for local documents and authoritative primary sources for external
technical references.

## Community Standards

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md). Use the public issue forms
for bugs and feature requests, [SUPPORT.md](SUPPORT.md) for help channels, and
[SECURITY.md](SECURITY.md) for private vulnerability reporting.
