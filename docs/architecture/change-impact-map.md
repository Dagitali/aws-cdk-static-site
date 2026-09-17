# Change-Impact Map

Use this map to identify the minimum complete change set. It describes ownership and review paths;
the current implementation, tests, Make targets, and workflows remain executable truth.

| Changed surface | Evidence to inspect | Validation | Documentation to review |
| --- | --- | --- | --- |
| `StaticSiteProps` field or validation | `props.py`, property tests, examples | unit and integration tests | configuration, API, design, changelog |
| Construct resource or behavior | `construct.py`, synthesis tests, `cdk-nag` expectations | unit, integration, optional security | architecture, costs, [Architecture Decision Records (ADRs)][ADRs], examples |
| Public export or typing | `__init__.py`, `py.typed`, artifact tests | typecheck, unit, distribution | API docs, quickstart, release notes |
| Example | example app and integration synthesis | `make test-examples` | examples index, Sphinx examples |
| Runtime dependency or Python range | `pyproject.toml`, lowest constraints, policy scripts | dependency policy and matrix-equivalent tests | README, testing, roadmap |
| Make target or test selection | `Makefile`, scripts, CI invocation | focused target plus local CI gate | AGENTS, contributing, testing |
| Workflow trigger, job, permission, or action | workflow YAML and policy tests | GitHub Actions pins and hosted dry run/PR | CI map, branch protection, runbooks |
| Release artifact or version behavior | CD workflow, setuptools-scm, artifact tests | distribution and installation tests | release policy, playbook, changelog |

- [Review Lenses](#review-lenses)
- [Boundary Rules](#boundary-rules)

## Review Lenses

For infrastructure changes, explicitly assess logical-ID replacement, IAM, public access, TLS and
DNS, data retention, custom resources, availability, and cost. For automation changes, assess event
scope, token permissions, immutable action pins, artifact provenance, required-check names, and
whether AWS credentials become reachable. For documentation-only changes, verify claims against
the executable source and check relative links; do not run cloud-changing validation.

## Boundary Rules

A consumer application owns accounts, regions, stack names, deployment identity, monitoring,
budgets, site content policy, and application APIs. This package owns the reusable construct and its
tested defaults. A proposed change that transfers one of those responsibilities needs explicit
design review and usually an ADR before implementation.

[ADRs]: ../decisions/README.md
