# 0003: Separate Validation from Cloud-Changing Automation

Status: Accepted

- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)
- [Alternatives Considered](#alternatives-considered)
- [References](#references)

## Context

Routine pull-request checks need deterministic feedback without exposing AWS credentials. A real
deployment test is still useful for the bounded integration that synthesis cannot prove.

## Decision

Keep normal CI, example synthesis, package validation, documentation builds, and `cdk-nag`
credential-free. Isolate AWS mutation in the manually dispatched disposable-deployment workflow,
restricted to `main`, an exact acknowledgement, a protected environment, short-lived OIDC
credentials, a fixed resource allowlist, and mandatory cleanup.

## Consequences

Pull requests cannot accidentally deploy resources. The manual test is slower and needs operator
approval and cleanup monitoring. Cancellation can still interrupt cleanup, so a narrowly scoped
recovery runbook is required.

## Alternatives Considered

Deploying on every pull request increases credential, cost, concurrency, and cleanup risk. Omitting
all deployment testing leaves a gap between synthesized intent and AWS behavior.

## References

- [CI/CD workflow map](../../CI-CD-WORKFLOWS.md)
- [Disposable deployment runbook](../runbooks/disposable-aws-deployment.md)
- [Deployment workflow](../../.github/workflows/deployment-test.yml)
