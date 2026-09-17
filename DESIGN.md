# Design

This document records the design principles and change constraints evident in the implementation,
tests, examples, and automation. See [Architecture] for the resulting resource and automation model.

- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Public API](#public-api)
- [Configuration Strategy](#configuration-strategy)
- [Caching and Content](#caching-and-content)
- [Security and Cost Defaults](#security-and-cost-defaults)
- [Testing and Change Safety](#testing-and-change-safety)
- [Decision Recording](#decision-recording)
- [Evolution Rules](#evolution-rules)

## Goals

- Provide a small, typed Python interface for a secure S3 and CloudFront static-site baseline.
- Support generated CloudFront hostnames, externally managed DNS, and Route 53-managed aliases.
- Make content deployment and access logging optional so consumers can choose their own workflows.
- Favor conservative durability, browser security, and cost defaults without claiming to be a
  complete production application platform.
- Remain independently testable through deterministic synthesis with no AWS credentials.

## Non-Goals

The construct does not parse environment variables or CDK context, create a consumer's CDK app,
provision GitHub OIDC roles, deploy production sites, or own account-wide budgets and controls. It
also excludes application APIs, analytics, SEO, branding, WAF, and organization-specific monitoring.
These concerns vary by consumer and would make the reusable construct harder to evolve safely.

## Public API

The package root intentionally exports only `StaticSite`, `StaticSiteProps`, and
`DEFAULT_CONTENT_SECURITY_POLICY`. `StaticSiteProps` is a frozen, slotted, keyword-only dataclass;
this makes configuration explicit and prevents mutation after validation. `StaticSite` publishes
resource handles so a consumer can add outputs, alarms, tags, grants, or dependencies.

The `src/` layout prevents accidental imports from the repository root. The `py.typed` marker and
strict mypy configuration make typing part of the supported package contract. Versions come from
Git tags through `setuptools-scm`, avoiding a second version source.

## Configuration Strategy

Configuration is supplied as Python objects, not read from process state. Validation rejects empty,
duplicate, incomplete, mutually exclusive, or region-incompatible values before synthesis proceeds.
Defaults work with CloudFront's generated hostname; each external integration is explicit.
The [configuration reference] documents the complete public property contract and validation rules.

Adding a property should follow this sequence:

1. Establish a demonstrated consumer requirement;
2. Select a safe, backwards-compatible default;
3. Validate invalid combinations in `StaticSiteProps`;
4. Synthesize the smallest required resource change in `StaticSite`;
5. Add property and synthesis tests plus a focused example when useful; and
6. Update configuration, API, architecture, cost, and changelog documentation as applicable.

## Caching and Content

HTML and the default behavior use disabled CloudFront caching to prioritize discoverable updates.
Static asset patterns use optimized edge caching. Built-in S3 deployment assigns short-lived,
must-revalidate browser metadata to mutable content and only assigns long-lived `immutable` metadata
to patterns selected by the consumer.

Immutable patterns must identify content-addressed filenames whose URLs change with their bytes.
Stable names such as `index.html`, `favicon.ico`, or `app.js` should not be immutable. Separate
deployments keep pruning and invalidation boundaries explicit.

## Security and Cost Defaults

- The origin bucket is private, encrypted, TLS-only, and served through OAC.
- The distribution redirects to HTTPS and uses TLS 1.2 (2021), modern HTTP versions, compression,
  IPv6, and browser-security headers.
- Content is retained and versioned by default; noncurrent versions expire after 30 days.
- Access logging is opt-in because it adds storage and privacy considerations; when enabled, log
  objects expire after a bounded period while the bucket itself is retained.
- `PriceClass_100` is the cost-conscious default. WAF, geo restrictions, and monitoring remain
  consumer decisions.
- Workflow permissions are job-scoped, third-party actions are pinned by full SHA, and the one
  deployment workflow uses short-lived OIDC credentials rather than stored AWS access keys.

These defaults are a baseline, not a certification. Consumers must review CSP origins, data
retention, availability, [costs], regulatory requirements, and organizational controls.

## Testing and Change Safety

Unit tests assert validation and stable CloudFormation properties. Integration tests synthesize
every example in an isolated output directory. Meta tests cover package artifacts, policy scripts,
and optional `cdk-nag`; end-to-end tests install built wheel and sdist artifacts outside the source
checkout. The default suite is credential-free and enforces at least 90% branch coverage.
The [testing guide] documents the executable test layers and commands.

Stateful-resource construct IDs are part of operational compatibility even when they are not part of
the Python API. Preserve them or add explicit regression coverage and migration guidance. Always
inspect synthesized changes for replacement, IAM permissions, custom resources, security, and cost.

## Decision Recording

Use `DESIGN.md` for current design rules and an [Architecture Decision Record (ADR)][architecture
decisions] for a decision whose alternatives or operational consequences must remain reviewable
after the implementation evolves. An ADR is appropriate when a change crosses ownership boundaries,
establishes a security or lifecycle default, constrains CI/CD, or would be expensive to reverse.
Keep status and supersession explicit; do not rewrite an accepted record to make history appear
cleaner.

The current ADR index documents the private OAC origin, retained stateful buckets, and separation of
credential-free validation from cloud-changing automation. See [architecture decisions].

## Evolution Rules

- Prefer additive optional properties over new mandatory inputs.
- Keep L2 constructs unless a documented requirement needs L1 or an escape hatch.
- Do not couple the library to one domain, account, repository, or content framework.
- Avoid duplicating tool configuration outside `pyproject.toml`.
- Keep normal CI offline with respect to AWS and reserve real deployments for explicit, bounded,
  reviewed workflows.
- Before 1.0, document breaking changes and migration steps; after 1.0, follow the repository's
  [release and deprecation policy].

[Architecture]: ARCHITECTURE.md
[architecture decisions]: docs/decisions/README.md
[configuration reference]: docs/CONFIGURATION.md
[costs]: docs/COSTS.md
[release and deprecation policy]: RELEASE-POLICY.md
[testing guide]: docs/TESTING.md
