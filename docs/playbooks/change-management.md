# Change Management Playbook

Use this playbook to connect change classification, supported scaffolding, documentation
synchronization, and release evidence. Branch, pull-request, tagging, and recovery mechanics remain
in the [maintainer runbooks].

- [Classify the Change](#classify-the-change)
- [Scaffold Only Supported Behavior](#scaffold-only-supported-behavior)
- [Synchronize Documentation](#synchronize-documentation)
- [Release and Rollback Evidence](#release-and-rollback-evidence)

## Classify the Change

| Class | Examples | Required evidence |
| --- | --- | --- |
| Public interface | Properties, validation, exports, typing | Contract tests, examples, compatibility review |
| Synthesized infrastructure | Resources, policies, caching, lifecycle | Synthesis tests, security review, replacement and cost assessment |
| Packaging | Dependencies, metadata, distributions | Boundary checks, artifact inspection, clean-install smoke tests |
| Delivery | Workflow triggers, permissions, release artifacts | Pin and policy checks, branch/environment review, rollback path |
| Documentation | Guides, examples, claims, links | Canonical-source review, local link checks, accessibility review |

Use the [change-impact map] to expand the selected class into the minimum complete implementation,
test, and documentation scope. A change spanning classes must satisfy each applicable evidence
boundary.

## Scaffold Only Supported Behavior

Before adding a component, configuration surface, example, or automation entry point, define:

- Its single responsibility and owner;
- Its public entry point and supported configuration;
- Its focused tests and credential-free local verification command;
- Its security, privacy, accessibility, lifecycle, availability, and cost boundaries;
- Its failure behavior, rollback approach, and documentation location; and
- Whether it belongs to the reusable construct or to a consuming application.

Do not add placeholder services, speculative public APIs, empty abstraction layers, or generic
runbooks without an operable use case. Preserve consumer ownership of accounts, deployment identity,
domains, content, monitoring, budgets, and application APIs. Follow the [API evolution checklist]
for changes to the construct's public or synthesized contract.

## Synchronize Documentation

Use the [documentation synchronization guide] during implementation rather than after it. Link to
authoritative detail instead of repeating it, and use the [evidence inventory template] in an
access-controlled system when a public claim depends on non-obvious evidence or disclosure
authority.

At minimum, recheck:

| If this changes | Recheck |
| --- | --- |
| Public property, validation, export, or default | API docstrings, configuration, examples, changelog |
| Resource, request, or lifecycle behavior | Architecture, design, costs, ADRs, synthesis assertions |
| Dependency, Python range, or artifact | Package metadata, lowest constraints, testing, release notes |
| Workflow, job, permission, or required check | CI map, branch protection, contributing, runbooks |
| Make target, script, or test layer | AGENTS, testing guides, CI callers, contributor commands |

Documentation-only work does not authorize implementation, workflow, AWS, DNS, publication, or
repository-setting changes.

## Release and Rollback Evidence

For a versioned release, use the [release notes template], [release checklist], and changelog.
Record:

- Exact scope and intentionally unchanged behavior;
- Compatibility, configuration, and migration requirements;
- Validation completed on the release candidate and checks still pending;
- Synthesized infrastructure, replacement, IAM, availability, security, and cost impact;
- Whether tagging publishes artifacts, deploys resources, changes DNS, or does neither; and
- A safe forward-fix or rollback path that respects immutable tags and retained data.

Do not infer deployed behavior from synthesis alone or claim release success before the exact
candidate passes its hosted checks and artifact validation. No step in this playbook authorizes an
AWS deployment, package publication, release tag, protected-branch mutation, or secret access.

[API evolution checklist]: ../api/evolution-checklist.md
[change-impact map]: ../architecture/change-impact-map.md
[documentation synchronization guide]: ../development/documentation-sync.md
[evidence inventory template]: ../EVIDENCE_INVENTORY_TEMPLATE.md
[maintainer runbooks]: ../runbooks/maintainer-operations.md
[release checklist]: release.md
[release notes template]: ../../.github/RELEASE-NOTES-TEMPLATE.md
