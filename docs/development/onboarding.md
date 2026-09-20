# Developer Onboarding

- [Prerequisites](#prerequisites)
- [First Local Session](#first-local-session)
- [Learn the Repository](#learn-the-repository)
- [Safe AWS Learning Path](#safe-aws-learning-path)
- [Pull Request Expectations](#pull-request-expectations)

## Prerequisites

- Git, GNU Make, and a Python version allowed by `pyproject.toml`;
- Node.js supported by the installed AWS CDK/jsii release; and
- AWS CLI v2 only for explicitly authorized AWS operations.

The package and its normal validation suite do not require AWS credentials. Treat the Python range
in `pyproject.toml`, rather than this guide, as the compatibility source of truth.

## First Local Session

```bash
make hooks
make check
```

`make hooks` creates `.venv`, installs the development dependency group, and installs the configured
commit-message, pre-commit, and pre-push hooks. Run `make help` to discover focused targets and
`make show-venv` to inspect the selected interpreter and environment paths.

## Learn the Repository

1. Read `AGENTS.md`, `ARCHITECTURE.md`, and `DESIGN.md`.
2. Use `docs/README.md` to find the maintained guide for the area you will change.
3. Inspect public implementation, tests, examples, and documentation together.
4. Run `git status --short` before editing and preserve unrelated work.
5. Use the verification matrix in `AGENTS.md` and report the commands actually run.

Useful focused loops include:

```bash
make test-unit
make test-integration
make test-examples
make docs-markdown
make docs-strict
```

`make check` is the normal local gate. Distribution installation and optional security tests remain
explicit because they install into clean environments or require additional dependency groups.

## Safe AWS Learning Path

Start with the examples and `make synth`; synthesis is deterministic and credential-free. Review the
generated CloudFormation before considering any deployed test. Do not learn by deploying,
destroying, changing DNS, or accessing credentials. The disposable deployment test is a separately
approved manual workflow with an exact acknowledgement, protected environment, fixed resource
allowlist, and mandatory cleanup.

## Pull Request Expectations

Use the GitFlow roles in `CONTRIBUTING.md`. A focused pull request explains compatibility and
synthesized-resource effects, validation, documentation updates, deployment or publication impact,
and rollback. Preserve stateful construct IDs and call out any intentional public API or generated
infrastructure change.
