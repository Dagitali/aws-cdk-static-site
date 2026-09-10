# Tests Overview

Tests are organized by scope rather than by feature. The root `conftest.py` assigns the matching
pytest marker from each test module's top-level directory.

- [Current Layout](#current-layout)
- [Discovery and Selection](#discovery-and-selection)
- [Dependency Prerequisites](#dependency-prerequisites)
- [Design Rules](#design-rules)
- [Common Commands](#common-commands)

## Current Layout

| Marker | Path | Purpose |
| --- | --- | --- |
| `unit` | `tests/unit/` | Fast, isolated configuration and synthesized-template behavior |
| `integration` | `tests/integration/` | Package behavior across documented example boundaries |
| `e2e` | `tests/e2e/` | Complete package workflows through a user-facing boundary |
| `meta` | `tests/meta/` | Distribution, repository-policy, and security-policy contracts |
| None | `tests/support/` | Shared constants, helpers, and fixtures; never collected as tests |

The scope answers how much of the system a test crosses. Module names describe what the test covers:

- `tests/integration/test_examples.py` synthesizes every example application;
- `tests/e2e/test_distribution_installation.py` installs each artifact in a clean environment;
- `tests/meta/test_package_artifacts.py` checks wheel, sdist, typing, legal, and metadata contracts;
- `tests/meta/test_cdk_nag.py` applies the optional synthesized-infrastructure policy.

## Discovery and Selection

Default discovery includes `tests/unit/` and `tests/integration/`. Select another layer by path or
select any collected layer by marker:

```bash
python -m pytest tests/unit
python -m pytest -m integration
python -m pytest --no-cov tests/meta/test_package_artifacts.py
python -m pytest --no-cov tests/e2e/test_distribution_installation.py
```

Artifact-oriented tests accept `--artifact-dir <path>` to reuse one wheel and one sdist. Without
that option, fixtures from `tests/support/artifacts.py` build both distributions once without build
isolation.

## Dependency Prerequisites

Install development dependencies before running default or artifact tests:

```bash
python -m pip install -e '.[dev]'
```

CI additionally runs Python 3.13 and 3.14 against the direct runtime dependency minima in
`requirements/lowest.txt` and against the newest stable versions permitted by `pyproject.toml`. Run
`make dependency-policy` to verify that the lowest constraints still match canonical metadata.

Install `.[security]` before running `tests/meta/test_cdk_nag.py`. Clean-install tests create their
own virtual environments and use the package index for runtime dependencies. Only the manually
approved deployment workflow requires AWS credentials.

## Design Rules

- Classify tests by `unit`, `integration`, `e2e`, or `meta` scope; express the subject in the module
  and test names.
- Keep fixtures at the narrowest useful scope and put genuinely shared test code in `support`.
- Name test modules for the production, integration, workflow, or repository contract they exercise.
- Assert stable public properties by default; pin logical IDs only for stateful resources whose
  replacement could risk persistent data.
- Keep unit and integration tests deterministic and independent of credentials and network access.
- Exercise built distributions outside the source checkout so editable imports cannot mask errors.
- Document every `cdk-nag` acknowledgment and fail on unreviewed findings.
- Keep integration fixtures local and independent of sibling repositories.

## Common Commands

```bash
make test
make test-unit
make test-integration
make test-examples
make test-distribution
make test-installation
make test-security
make test-full
```

See the [testing guide](../docs/TESTING.md) for layer ownership, CI placement, coverage semantics,
and the deployed-resource boundary.
