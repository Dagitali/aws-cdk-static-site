# Testing Guide

The test strategy uses the conventional unit, integration, end-to-end, and meta layers. A suite runs
only where its dependencies and side effects are explicit.

- [Set Up Development](#set-up-development)
- [Test Layers](#test-layers)
- [Focused Suites](#focused-suites)
- [Run Checks](#run-checks)
- [Test Design](#test-design)
- [AWS Deployment Boundary](#aws-deployment-boundary)

## Set Up Development

The package metadata in `pyproject.toml` supports Python 3.13 and 3.14, while `.python-version`
selects Python 3.13 for compatible local version managers. Package versions are derived from Git
tags by `setuptools-scm`; local builds after the latest tag receive a development version.

```bash
make dev
```

Install the optional `cdk-nag` dependency only when running its meta test:

```bash
python -m pip install -e '.[security]'
```

## Test Layers

| Layer | Path | Contract | Default |
| --- | --- | --- | --- |
| Unit | `tests/unit/` | Isolated package behavior and synthesized resource properties | Yes |
| Integration | `tests/integration/` | Interactions with examples and consumer content | Yes |
| End to end | `tests/e2e/` | Complete local package workflows across process boundaries | Explicit CI job |
| Meta | `tests/meta/` | Distribution, repository-policy, and security-policy contracts | By suite |
| Support | `tests/support/` | Shared non-test constants, helpers, and fixtures | Never collected |

Directory-based markers are applied centrally by `tests/conftest.py`. Default pytest discovery is
limited to unit and integration tests so local test runs remain credential-free and deterministic.
The `support` directory is importable test infrastructure, not another test layer.

## Focused Suites

| Suite | Location | Execution |
| --- | --- | --- |
| Example synthesis | `tests/integration/test_examples.py` | Default suite |
| `dagitali.com` consumer | `tests/integration/test_dagitali_com.py` | Default skip or dedicated CI job |
| Artifact installation | `tests/e2e/test_distribution_installation.py` | Distribution CI job |
| Artifact contracts | `tests/meta/test_package_artifacts.py` | Distribution and release jobs |
| `cdk-nag` policy | `tests/meta/test_cdk_nag.py` | Optional manual security job |
| Disposable AWS deployment | `.github/workflows/deployment-test.yml` | Manual approval only |

Artifact installation and contract tests accept `--artifact-dir` to reuse distributions built once
by CI or the release workflow. Fixtures and helpers for this behavior live in
`tests/support/artifacts.py`.

The consumer test defaults to the adjacent `../dagitali.com` checkout. Set `DAGITALI_COM_PATH` or
`CONSUMER_PROJECT_DIR` when the consumer lives elsewhere. Because dagitali.com has not yet migrated
to this package, this layer validates that the construct can synthesize its real site content and
external-DNS delivery shape; it does not claim that dagitali.com's current stack imports the
construct.

## Run Checks

Run the default local gate and CI-oriented documentation and distribution checks:

```bash
make check
make check-ci-local
```

Run focused suites explicitly:

```bash
make test-unit
make test-integration
make test-examples
make test-distribution
make test-installation
make test-consumer
make test-security
make test-full
```

`make test-installation` accesses the package index to install runtime dependencies into clean
virtual environments. `make test-security` installs the optional security dependency group. The
normal test command enforces branch coverage with a 90% minimum; subprocess and optional layers use
`--no-cov` and do not dilute the unit-test coverage measurement.

Coverage, pytest, Ruff, and mypy settings are centralized in `pyproject.toml`. The project does not
duplicate these settings in `.coveragerc`, `pytest.toml`, `pytest.ini`, `ruff.toml`, or `.ruff.toml`.

## Test Design

- Choose `unit`, `integration`, `e2e`, or `meta` from the execution boundary, then name the module
  for the behavior or contract under test.
- Group cohesive behaviors in test classes and parameterize repeated contracts.
- Put code in `tests/support/` only when multiple tests or layers genuinely share it.
- Assert stable resource properties rather than generated logical IDs, except for stateful-resource
  identity regression tests.
- Keep unit and integration tests independent of AWS credentials and network access.
- Build distributions once per test session and install them outside the source checkout.
- Treat every security acknowledgment as a reviewed design decision with a concrete reason.
- Keep consumer fixtures read-only and make missing local consumers an explicit skip.

## AWS Deployment Boundary

Normal pytest and CI never deploy resources. The manual workflow is restricted to `main`, requires
the exact `DEPLOY-AND-DESTROY` acknowledgement and a protected GitHub environment, validates a fixed
resource allowlist before deployment, and waits for stack deletion afterward. See [Disposable AWS
Deployment Testing](DEPLOYMENT-TESTING.md) before configuring or running it.
