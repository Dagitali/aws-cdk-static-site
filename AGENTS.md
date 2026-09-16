# AGENTS

These instructions apply to automated coding agents working in this repository. User and
system-level instructions take precedence.

- [Repository Boundaries](#repository-boundaries)
- [Agent Operating Model](#agent-operating-model)
- [Repository Map](#repository-map)
- [Development Policy](#development-policy)
- [Validation Commands](#validation-commands)
- [AWS CDK Conventions](#aws-cdk-conventions)
- [Documentation Obligations](#documentation-obligations)
- [Git and Automation](#git-and-automation)
- [Release Readiness](#release-readiness)
- [Infrastructure Safety](#infrastructure-safety)
- [Definition of Done](#definition-of-done)
- [Completion Report](#completion-report)

## Repository Boundaries

- Treat `pyproject.toml` as the canonical source for package metadata and Python-tool configuration.
- Derive package versions from Git tags through `setuptools-scm`; do not add a second version
  source.
- Preserve the `src/` package layout and the intentional exports in the package root's `__all__`.
- Keep reusable construct behavior separate from consumer-owned CDK app configuration, website
  content, deployment identity, monitoring, and account-wide controls.
- Preserve unrelated working-tree changes and generated or user-owned files.
- Treat `docs/build/`, `dist/`, `cdk.out/`, caches, virtual environments, and egg metadata as
  generated output. Do not edit or commit them as source documentation.
- Do not change public API, synthesized resources, workflow permissions, release behavior, or AWS
  state merely to satisfy a documentation task.

## Agent Operating Model

Before editing:

1. Read this file and any more specific `AGENTS.md` in the target subtree.
2. Inspect `git status --short` and preserve unrelated changes. Never discard, overwrite, stage, or
   reformat files outside the task's scope.
3. Trace claims to repository evidence. For construct behavior, read `props.py`, `construct.py`, and
   relevant tests; for commands, read `Makefile`; for automation, read the workflow itself.
4. State the intended file scope and the narrowest verification that can prove the change.

While editing:

- Prefer a focused diff over broad cleanup. Preserve established terminology and relative links.
- Do not invent deployed topology, account details, release state, pricing, or future commitments.
- Record assumptions as assumptions. Convert durable architectural choices into ADRs and reusable
  troubleshooting outcomes into `LEARNINGS.md`.
- Stop and request explicit authorization before an AWS deploy or destroy, package publication,
  release/tag creation, protected-branch mutation, secret access, or any destructive operation.
- If repository evidence conflicts, report the conflict and fix the narrowest authoritative source;
  do not silently choose the more convenient claim.

Use ChatGPT for exploratory architecture discussion, alternatives, risk review, and decision framing
when no repository write is required. Use Codex for evidence-backed repository inspection, edits,
tests, and diffs. A ChatGPT conclusion is input to review, not repository truth, until Codex
confirms it against the current checkout and records the accepted result. See the [agent workflow]
and [task templates].

## Repository Map

- `src/aws_cdk_static_site/` contains the public `StaticSite` construct and immutable
  `StaticSiteProps` configuration. Keep the public facade in `__init__.py` intentional.
- `tests/unit/` verifies isolated behavior and synthesized resource properties.
- `tests/integration/` synthesizes every example; `tests/e2e/` verifies built distributions.
- `tests/meta/` enforces packaging, repository, and optional `cdk-nag` contracts.
- `tests/support/` contains shared test infrastructure and must not be collected as a test layer.
- `examples/` demonstrates supported compositions. Examples are documentation and test fixtures, not
  production stacks.
- `scripts/` implements repository-policy checks exposed through `python -m scripts` and Make.
- `docs/source/` is the Sphinx source; `docs/build/` is generated and must not be edited.
- `.github/workflows/` separates PR routing, CI, releases, SBOM generation, optional security
  checks, and the guarded disposable deployment test.

## Development Policy

- Use a Python version permitted by `project.requires-python` in `pyproject.toml` and retain the
  repository's supported-version policy checks.
- Add or update tests for changed public behavior, validation, and synthesized infrastructure.
- Keep unit tests deterministic and independent of AWS credentials, deployed resources, and network
  access.
- Run the narrowest relevant checks while iterating and `make check` before completing a change when
  practical.
- Update public documentation and `CHANGELOG.md` when user-visible behavior changes.
- Keep remote GitHub Actions pinned to full commit SHAs.

Follow the established Python style:

- Target Python 3.13 syntax while preserving the declared `>=3.13,<3.15` support range;
- Use single-quoted strings and an 88-character line length;
- Keep mypy strict and avoid untyped public surfaces;
- Use NumPy-style public docstrings and the existing section comments where they aid navigation; and
- Prefer immutable, keyword-only configuration objects and validation before resource creation.

## Validation Commands

Use Make targets as the stable contributor interface:

| Change | Minimum focused validation |
| --- | --- |
| Python implementation | `make lint typecheck test-unit` |
| Construct or configuration behavior | `make test-unit test-integration` |
| Example | `make test-examples` |
| Workflow | `make workflow-pins python-policy` |
| Dependencies or packaging | `make dependency-policy test-distribution` |
| Documentation | `make docs-strict` |
| Broad or release-sensitive change | `make check-ci-local` |

Run `make check` before completion when practical. The default pytest suite covers unit and
integration tests with at least 90% branch coverage; optional security, distribution, and
installation suites must be invoked explicitly.

For Markdown-only changes outside `docs/source/`, also run a repository-local Markdown structure and
relative-link check when available. `make docs-strict` validates Sphinx sources; it does not prove
that every standalone Markdown link resolves.

## AWS CDK Conventions

- Prefer stable L2 constructs and explicit typed properties. Use L1 constructs or escape hatches
  only when required and document why.
- Preserve construct IDs for stateful resources. Renaming or moving constructs can change logical
  IDs and replace resources; protect such changes with synthesis assertions and review `cdk diff`.
- Keep the S3 origin private and reachable through CloudFront Origin Access Control.
- Retained, versioned content storage is the default. A destructive removal policy alone does not
  empty a non-empty bucket, and this construct deliberately leaves `auto_delete_objects=False`.
- CloudFront custom-domain certificates must be in `us-east-1`. Construct-managed certificate
  creation requires a concrete `us-east-1` stack environment.
- Keep account-wide controls, budgets, application APIs, monitoring, GitHub deployment roles, and
  consumer configuration outside this reusable construct unless its public boundary is revised.
- Assert stable resource properties rather than generated logical IDs, except for tests that
  intentionally guard a stateful resource identity.

## Documentation Obligations

Update documentation in the same change when its source of truth changes:

| Change | Documentation to review |
| --- | --- |
| Public property, validation, or export | Docstrings, `docs/CONFIGURATION.md`, `docs/api/`, examples, changelog |
| Resource, request, lifecycle, or trust boundary | `ARCHITECTURE.md`, `DESIGN.md`, costs, tests, relevant ADR |
| Make target or test layer | `AGENTS.md`, `CONTRIBUTING.md`, `docs/TESTING.md`, CI map |
| Workflow trigger, job name, permissions, or artifact | `CI-CD-WORKFLOWS.md`, runbooks, branch-protection docs |
| Release behavior or compatibility promise | `RELEASE-POLICY.md`, release playbook, roadmap, changelog |
| Reusable failure and recovery | `LEARNINGS.md` and, when operational, a runbook |

Do not duplicate generated API reference. Update public docstrings and `docs/source/` inputs. Follow
the [documentation synchronization guide] for ownership, drift checks, and link validation.

## Git and Automation

- Follow the GitFlow routes enforced by `.github/workflows/pr.yml`: feature, bugfix, chore, CI,
  docs, Dependabot, and sync branches target `develop`; release and hotfix branches target `main`.
- Do not commit directly to `develop` or `main`; local hooks and hosted checks enforce this.
- Use Conventional Commits and align release notes and `CHANGELOG.md` with user-visible changes.
- Never weaken least-privilege workflow permissions or replace pinned action SHAs with floating tags
  without an explicit, reviewed policy change.
- Normal CI must remain credential-free and deployment-free. The manual deployment test is a
  separately approved exception with a fixed resource allowlist and mandatory cleanup.

## Release Readiness

For changes affecting packaging, releases, compatibility, versioned documentation, or CI/CD, consult
the [release policy] and the [release checklist].

Preserve these release safeguards unless the user explicitly changes the policy:

- build both the source distribution and wheel;
- validate distributions with `twine check`;
- smoke-test each built distribution in an isolated clean environment;
- create annotated release tags on authoritative commits merged into `main`; and
- publish through reviewed automation and trusted identity rather than long-lived credentials.

The project is not yet published to PyPI. Do not publish artifacts or configure external release
credentials unless the user explicitly authorizes that work.

## Infrastructure Safety

- Synthesize and inspect CloudFormation before proposing deployment-sensitive changes.
- Do not deploy, destroy, or modify AWS resources unless the user explicitly requests the external
  operation.
- Do not expose AWS account identifiers, credentials, private domain data, or synthesized templates
  containing sensitive values.
- Document resource replacement, security, availability, and cost implications when construct
  behavior changes.

## Definition of Done

A change is complete when all applicable items are true:

- Implementation, tests, examples, and public documentation agree;
- Focused checks pass, followed by `make check` or `make check-ci-local` for broad changes;
- Synthesized changes were inspected for replacement, IAM, security, availability, and cost impact;
- Public behavior changes include tests and an `Unreleased` changelog entry;
- Workflow edits retain full-SHA action pins and least-privilege permissions;
- Generated files, credentials, account identifiers, and unrelated working-tree changes were not
  added; and
- No AWS deployment, destruction, publication, tag creation, or external release occurred without
  explicit user authorization.

## Completion Report

Report:

- Files created, updated, and intentionally left untouched;
- The evidence and rationale for each major decision;
- Validation commands run and their results;
- Skipped checks with a concrete reason; and
- Remaining risks, assumptions, or follow-up work.

Do not claim success from edits alone. Distinguish completed validation from recommended validation,
and never hide a failing check behind a broader passing command.

[agent workflow]: docs/development/agent-workflow.md
[documentation synchronization guide]: docs/development/documentation-sync.md
[release checklist]: docs/playbooks/release.md
[release policy]: RELEASE-POLICY.md
[task templates]: docs/development/codex-task-templates.md
