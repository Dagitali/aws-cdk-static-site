# Documentation

Use this directory for maintained project guides and reference material. Repository governance and
community policies remain at the repository root or under `.github/` so their conventional paths
are discoverable by contributors and GitHub.

- [Document Scope](#document-scope)
- [Build the Local Site](#build-the-local-site)
- [Guides](#guides)
- [Related Repository Documents](#related-repository-documents)

## Document Scope

Root-level community and lifecycle documents define conventions that can be shared across projects,
with repository-specific names, links, support boundaries, and release state supplied locally. Files
under `.github/` describe GitHub-facing policy and must remain synchronized with actual workflow and
ruleset names. Guides in `docs/` describe this package and should not be generalized at the expense
of accurate product behavior.

## Build the Local Site

The lightweight Sphinx site combines a short getting-started path, focused examples, and API
documentation generated from package docstrings. Build the HTML site locally with:

```bash
make docs
```

Use the CI-parity build, which treats warnings as errors, before proposing documentation changes:

```bash
make docs-markdown
make docs-strict
```

The Markdown check validates local paths and heading anchors across the repository without network
access. The strict Sphinx build validates generated API documentation and its source tree.

Additional builders exercise output formats and external links:

```bash
make docs-epub
make docs-linkcheck
```

Open `docs/build/html/index.html` after an HTML build completes. Generated output under
`docs/build/` is ignored by Git. Read the Docs configuration and publication are intentionally
deferred until this package has a regular PyPI release lifecycle; CI builds the same HTML sources
only to prevent documentation regressions.

## Guides

- [Architecture] describes the resource model, request flow, lifecycle, and automation boundaries.
- [Design] records public API principles, configuration strategy, defaults, and evolution rules.
- [Configuration] describes construct properties, valid combinations, and DNS
  ownership models.
- [Costs] explains cost drivers and safeguards without promising fixed prices.
- [Testing] covers local quality gates and test design.
- [Developer onboarding] provides the shortest safe path to a working local environment.
- [Agent workflow] defines evidence gathering, tool roles, safe editing, and completion reporting.
- [Documentation synchronization] maps executable sources to the prose that must change with them.
- [Evidence inventory template] provides a privacy-aware review record for proposed public claims.
- [Codex task templates] provides reusable prompts with scope, safety, and verification fields.
- [Disposable AWS deployment testing] defines the manual test's identity, resource, cost, and
  cleanup boundaries.
- [Project roadmap] records current status, consumer validation, and publication planning.
- [Construct extraction history] preserves the completed origin and extraction milestones.
- [Learnings] captures reusable symptom, cause, fix, and verification records.
- [Release notes archive] indexes detailed committed records for each release candidate.
- [Examples] demonstrates supported composition patterns.
- [Consumer tutorial] walks from a new CDK app to credential-free synthesis.
- [Consumer scaffolding] turns a new consumer requirement into a reviewable project baseline.
- [Change management] connects change classification, supported scaffolding, documentation, and
  release evidence.
- [Incident response] covers failures in CI, releases, packages, and the disposable deployment test.

Topic indexes reserve discoverable homes for documentation as it grows:

- [API notes] for maintained public-interface design notes;
- [Architecture notes] for focused diagrams and analyses;
- [Decision records] for durable architectural decisions;
- [Development documentation] for detailed contributor guidance;
- [Playbooks] for repeatable maintainer workflows;
- [Runbooks] for bounded operational procedures; and
- [Tutorials] for end-to-end consumer learning paths.

## Related Repository Documents

- [Contributing]
- [CI/CD workflow map]
- [Release policy]
- [Release checklist]
- [Maintainer runbooks]
- [Support]
- [Security]
- [Technical references]

Keep examples executable, prefer relative links between repository documents, and verify
pricing-sensitive or service-specific claims against the authoritative source linked in
`REFERENCES.md`.

[API notes]: api/README.md
[Architecture]: ../ARCHITECTURE.md
[Architecture notes]: architecture/README.md
[Agent workflow]: development/agent-workflow.md
[CI/CD workflow map]: ../CI-CD-WORKFLOWS.md
[Configuration]: CONFIGURATION.md
[Contributing]: ../CONTRIBUTING.md
[Costs]: COSTS.md
[Construct extraction history]: architecture/construct-extraction-history.md
[Consumer scaffolding]: playbooks/scaffold-consumer-project.md
[Consumer tutorial]: tutorials/synthesize-first-site.md
[Change management]: playbooks/change-management.md
[Codex task templates]: development/codex-task-templates.md
[Disposable AWS deployment testing]: runbooks/disposable-aws-deployment.md
[Documentation synchronization]: development/documentation-sync.md
[Evidence inventory template]: EVIDENCE_INVENTORY_TEMPLATE.md
[Decision records]: decisions/README.md
[Development documentation]: development/README.md
[Developer onboarding]: development/onboarding.md
[Design]: ../DESIGN.md
[Examples]: ../examples/README.md
[Maintainer runbooks]: runbooks/maintainer-operations.md
[Incident response]: runbooks/incident-response.md
[Learnings]: ../LEARNINGS.md
[Release checklist]: playbooks/release.md
[Release notes archive]: releases/README.md
[Release policy]: ../RELEASE-POLICY.md
[Project roadmap]: ../ROADMAP.md
[Playbooks]: playbooks/README.md
[Runbooks]: runbooks/README.md
[Security]: ../SECURITY.md
[Support]: ../SUPPORT.md
[Technical references]: ../REFERENCES.md
[Testing]: TESTING.md
[Tutorials]: tutorials/README.md
