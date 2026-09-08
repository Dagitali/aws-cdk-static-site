# Tests Overview

Tests are organized by scope and labeled with pytest markers.

- [Current Layout](#current-layout)
- [Discovery and Selection](#discovery-and-selection)
- [Dependency Prerequisites](#dependency-prerequisites)
- [Design Rules](#design-rules)
- [Common Commands](#common-commands)
- [Future Test Levels](#future-test-levels)

## Current Layout

| Marker | Path | Purpose |
| --- | --- | --- |
| `unit` | `tests/unit/` | Fast, isolated validation and CDK synthesis behavior |
| `integration` | `tests/integration/` | Synthesis across the installed package and runnable examples |

The marker registry and default discovery paths are defined in `pyproject.toml`.

## Discovery and Selection

The default `pytest` invocation discovers tests under `tests/`. Select the current scope by path or
marker:

```bash
python -m pytest tests/unit
python -m pytest -m unit
python -m pytest tests/integration
python -m pytest -m integration
```

Keep path-based scope and scope-marker selection equivalent as new test levels are introduced.

## Dependency Prerequisites

Install the development dependency group before running tests:

```bash
python -m pip install -e '.[dev]'
```

The unit and integration suites synthesize CDK constructs locally and do not require AWS
credentials, a bootstrapped account, or network access. The integration suite runs each documented
example as an independent application. Its focused Make target disables in-process coverage because
the package code runs in subprocesses; default discovery still enforces the configured threshold.

## Design Rules

- Name test modules after the production module they exercise.
- Group cohesive behavior in test classes and parameterize repeated contracts.
- Assert stable public properties by default; pin generated logical IDs only for stateful resources
  whose accidental replacement could risk persistent data.
- Keep unit tests deterministic and independent of AWS credentials and network access.
- Use fixtures for shared setup without hiding the behavior under test.

## Common Commands

```bash
make test
make test-unit
make test-integration
make test-full
```

Use `make test-unit` or `make test-integration` for a focused scope, `make test` for default pytest
discovery, and `make test-full` for every test target available to the project. Run `make check` for
the complete local quality gate.

## Future Test Levels

Add `tests/e2e/` only for a bounded deployed fixture owned by this repository. Add `tests/meta/` for
repository-policy tests when those checks are better expressed in pytest than in focused scripts.

Scope markers should describe where a test operates; intent markers such as `smoke` or `contract`
may be added later when multiple tests need that cross-cutting selection.
