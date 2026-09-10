# Contributing Guidelines

Contributions to source code, tests, documentation, and repository automation are welcome through
GitHub issues and pull requests. By submitting a contribution, you agree that it may be distributed
under this project's [MIT License](LICENSE).

- [Ways to Contribute](#ways-to-contribute)
- [Development Workflow](#development-workflow)
- [Protected-Branch GitFlow](#protected-branch-gitflow)
- [Public API and Type Checking](#public-api-and-type-checking)
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

## Public API and Type Checking

Names exported through the package root's `__all__` form its intentional package-level public API.
Treat changes to their names, signatures, defaults, validation, and documented behavior as
compatibility decisions rather than internal refactors. For an infrastructure library, documented
synthesized behavior is also part of that compatibility review.

The package ships a `py.typed` marker and runs mypy in strict mode. When contributing Python code:

- Use syntax supported by the minimum Python version declared in `pyproject.toml`;
- Prefer precise boundary types over `Any` and explain unavoidable dynamic boundaries;
- Keep runtime validation for configuration rules that type checking cannot enforce;
- Avoid importing internal modules in examples when the package-level API is sufficient; and
- Add contract tests when changing public configuration or generated infrastructure.

Run `make typecheck` locally and include migration guidance for intentional breaking changes.

## Local Quality Gates

Run the default local gate with:

```bash
make check
```

Run the CI-equivalent gate, including the strict HTML documentation build, with:

```bash
make check-ci-local
```

Useful focused targets include:

```bash
make fmt
make lint
make typecheck
make test
make test-distribution
make test-installation
make test-security
make docs-strict
make docs-linkcheck
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

Keep artifact installation, optional security checks, and deployed tests in their documented layers
so normal unit and integration runs remain deterministic. Never run or broaden the disposable AWS
deployment test without reviewing its identity, resource, cost, and cleanup boundaries.

See [docs/TESTING.md](docs/TESTING.md) and [tests/README.md](tests/README.md) for test organization,
markers, and commands.

## Documentation

Keep prose concise, use descriptive link text, and wrap code, file names, commands, and identifiers
in backticks. Update nearby examples and cross-references when behavior or public interfaces change.
Prefer repository-relative links for local documents and authoritative primary sources for external
technical references.

Document public behavior and decision-relevant constraints rather than restating implementation line
by line. Keep headings in title case, preserve the official capitalization of tools and products,
and keep table-of-contents labels synchronized with their headings.

## Community Standards

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md). Use the public issue forms
for bugs and feature requests, [SUPPORT.md](SUPPORT.md) for help channels, and
[SECURITY.md](SECURITY.md) for private vulnerability reporting.
