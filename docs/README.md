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
documentation generated from package docstrings. Build it locally with warnings treated as errors:

```bash
make docs-strict
```

Open `docs/build/html/index.html` after the build completes. The generated site is ignored by Git.
Read the Docs configuration and publication are intentionally deferred until this package has a
regular PyPI release lifecycle; CI builds the same sources only to prevent documentation
regressions.

## Guides

- [Configuration](CONFIGURATION.md) describes construct properties, valid combinations, and DNS
  ownership models.
- [Costs](COSTS.md) explains cost drivers and safeguards without promising fixed prices.
- [Testing](TESTING.md) covers local quality gates and test design.
- [Roadmap](ROADMAP.md) records the extraction and stabilization plan.
- [Examples](../examples/README.md) demonstrates supported composition patterns.

## Related Repository Documents

- [Contributing](../CONTRIBUTING.md)
- [CI/CD workflow map](../CI-CD-WORKFLOWS.md)
- [Release policy](../RELEASE-POLICY.md)
- [Release checklist](../RELEASE-CHECKLIST.md)
- [Maintainer runbooks](../.github/MAINTAINER-RUNBOOKS.md)
- [Support](../SUPPORT.md)
- [Security](../SECURITY.md)
- [Technical references](../REFERENCES.md)

Keep examples executable, prefer relative links between repository documents, and verify
pricing-sensitive or service-specific claims against the authoritative source linked in
`REFERENCES.md`.
