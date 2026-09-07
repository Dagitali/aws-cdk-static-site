# Testing Guide

The test suite verifies public configuration contracts and synthesized CloudFormation without
deploying resources or calling AWS. These are unit tests because the external AWS boundary is
represented by CDK constructs and assertions.

- [Set Up Development](#set-up-development)
- [Run checks](#run-checks)
- [Test Design](#test-design)
- [Future Test Levels](#future-test-levels)

## Set Up Development

The package metadata in `pyproject.toml` supports Python 3.13 and newer, while `.python-version`
selects Python 3.13 as the consistent local development version for compatible tools such as pyenv
and uv. The files are complementary: one declares package compatibility, and the other selects an
interpreter.

Package versions are also derived from Git tags by `setuptools-scm`. Local builds after the latest
tag receive a development version; an authoritative release build must come from its annotated
`v<version>` tag.

```bash
make dev
```

## Run checks

Run the complete local gate:

```bash
make check
```

Run focused checks:

```bash
make lint
make typecheck
make test
make test-unit
make test-full
make dist
make package
make workflow-pins
make python-policy
```

The normal test command enforces branch coverage with a 90% minimum. Coverage, pytest, Ruff, and
mypy settings are centralized in `pyproject.toml`; pytest uses the native pytest 9 `[tool.pytest]`
table, and Ruff uses `[tool.ruff]` and its subtables as the canonical linting and formatting policy.
The project does not duplicate these settings in `.coveragerc`, `pytest.toml`, `pytest.ini`,
`ruff.toml`, or `.ruff.toml`. Flake8 is neither installed nor configured because Ruff provides the
project's linting policy.

## Test Design

- Name test modules after production modules.
- Group cohesive behaviors in test classes.
- Parameterize repeated input/output contracts.
- Assert stable resource properties rather than generated logical IDs.
- Avoid AWS credentials and network access in unit tests.
- Test validation failures as part of the public API contract.

`tests/unit/test_construct.py` verifies storage, delivery, deployment, DNS, certificate, and logging
behavior. `tests/unit/test_props.py` verifies configuration defaults and invalid combinations.

## Future Test Levels

Add integration tests when `dagitali.com` consumes the package. Those tests should compare relevant
synthesized behavior before and after migration and smoke-test a wheel-installed consumer in a clean
environment. Add deployed end-to-end tests only when this repository owns a bounded test fixture or
example deployment; production website checks should otherwise remain in the consuming repository.
