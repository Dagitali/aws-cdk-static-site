# Documentation Synchronization

Documentation changes are complete when the maintained prose agrees with executable sources and
relative links resolve. Generated output under `docs/build/` is never a source of truth.

- [Ownership Map](#ownership-map)
- [Change Procedure](#change-procedure)
- [Documentation-Only Boundary](#documentation-only-boundary)
- [Completion Evidence](#completion-evidence)

## Ownership Map

| Claim | Canonical evidence | Maintained mirrors to review |
| --- | --- | --- |
| Package metadata, Python range, dependencies | `pyproject.toml` | README, testing, roadmap, Sphinx getting started |
| Contributor command | `Makefile` and invoked script | AGENTS, contributing, testing, playbooks |
| Public API and validation | source docstrings, implementation, tests | configuration, API notes, examples, Sphinx |
| Synthesized resource behavior | construct plus synthesis tests | architecture, design, costs, [Architecture Decision Records (ADRs)][ADRs] |
| Workflow trigger, job, permission, artifact | `.github/workflows/*.yml` | CI map, branch protection, runbooks |
| Release and version behavior | tags, setuptools-scm, CD workflow | release policy, playbook, changelog, release archive |
| Current priorities | `ROADMAP.md` | link to it; do not create a second active roadmap |

## Change Procedure

1. Locate every repository reference to the changed name or claim.
2. Read the canonical source rather than copying another guide.
3. Update the smallest set of maintained mirrors; link instead of duplicating large reference text.
4. Add an ADR for durable alternatives/consequences or a learning for a reusable diagnosed failure.
5. Run `make docs-markdown` for repository-local Markdown links and heading anchors.
6. Run `make docs-strict` when Sphinx sources, public docstrings, or their dependencies changed.
   Treat external link checks as advisory because remote availability can be transient.
7. Inspect the diff for private identifiers, fixed prices, unverified future state, and stale names.

## Documentation-Only Boundary

A docs task does not authorize changes to code, synthesized infrastructure, workflows, AWS state,
repository settings, releases, or credentials. If accurate documentation would require one of those
changes, report the mismatch and split the implementation into a separately authorized task.

## Completion Evidence

List created and updated files, the source used for each major claim, commands run, and skipped
checks. State whether the change affects public behavior; if it does not, say so explicitly.

[ADRs]: ../decisions/README.md
