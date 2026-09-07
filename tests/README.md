# Tests Overview

Tests are organized by scope and labeled with pytest markers.

- [Current Layout](#current-layout)
- [Design Rules](#design-rules)
- [Commands](#commands)
- [Future Test Levels](#future-test-levels)

## Current Layout

| Marker | Path | Purpose |
| --- | --- | --- |
| `unit` | `tests/unit/` | Fast, isolated validation and CDK synthesis behavior |

The marker registry and default discovery paths are defined in `pyproject.toml`.

## Design Rules

- Name test modules after the production module they exercise.
- Group cohesive behavior in test classes and parameterize repeated contracts.
- Assert stable public properties instead of generated logical IDs.
- Keep unit tests deterministic and independent of AWS credentials and network access.
- Use fixtures for shared setup without hiding the behavior under test.

## Commands

```bash
make test
make test-unit
make test-full
```

Run `make check` for the complete local quality gate.

## Future Test Levels

Add `tests/integration/` when verifying interactions across package or consumer boundaries, and add
`tests/e2e/` only for a bounded deployed fixture owned by this repository. Add `tests/meta/` for
repository-policy tests when those checks are better expressed in pytest than in focused scripts.

Scope markers should describe where a test operates; intent markers such as `smoke` or `contract`
may be added later when multiple tests need that cross-cutting selection.
