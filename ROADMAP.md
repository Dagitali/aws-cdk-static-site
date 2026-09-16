# Roadmap

This is the canonical active roadmap for the project. It reflects repository evidence as of the
current pre-1.0 development line; it is not a promise of dates. The completed origin and extraction
phases are retained separately as [construct extraction history].

- [Current State](#current-state)
- [Near Term](#near-term)
- [Before PyPI](#before-pypi)
- [Later Opportunities](#later-opportunities)
- [Completed Foundations](#completed-foundations)
- [Historical Context](#historical-context)

## Current State

- The reusable `StaticSite` construct covers private S3 storage, CloudFront OAC delivery, security
  headers, mutable and immutable cache behavior, optional local content deployment, optional
  retained access logs, and optional ACM and Route 53 integration.
- The public package is alpha/pre-1.0 and supports Python 3.13 and 3.14 with AWS CDK v2.
- GitHub Releases are the supported distribution surface. Package versions are derived from tags;
  PyPI publication is intentionally inactive.
- CI exercises source quality, strict typing, 90% branch coverage, example synthesis, documentation,
  supported Python/dependency boundaries, package artifacts, and clean installation.
- Optional `cdk-nag` and a guarded disposable AWS deployment workflow provide additional confidence
  without giving routine CI cloud credentials.
- `dagitali.com` has adopted a pinned release of the construct while retaining application-owned
  concerns and deployed resource identities.
- The current checkout is on `develop`; release and hotfix changes use the documented GitFlow.

## Near Term

- Continue validating the `dagitali.com` adoption and feed reusable lessons back into this package.
- Create `datasci.me`, then use the [construct-adoption playbook] to validate the API with a second,
  materially different static-site consumer.
- Review whether the default security policy remains practical for consumers using fonts,
  analytics, forms, or third-party media.
- Convert demonstrated consumer needs into small, optional extension points rather than speculative
  framework features.
- Keep contact APIs, budgets, and deployment workflows outside the core construct unless repeated
  consumer evidence supports separate reusable packages or examples.

## Before PyPI

- Recheck package-name availability immediately before publication.
- Review and document the supported public API and compatibility commitments.
- Review the locally generated API documentation as part of public API stabilization.
- Complete first- and second-consumer validation and resolve discovered ergonomics gaps.
- Configure PyPI Trusted Publishing through a protected GitHub environment; do not introduce
  long-lived credentials or manual uploads.
- Publish a prerelease and validate installation, metadata, wheel, sdist, checksums, SBOM, and basic
  synthesis from the published artifact.
- Retain tag-triggered validation that builds and installs the wheel and sdist, checks metadata,
  synthesizes a representative example, and publishes GitHub Release assets.
- Publish the CI-validated Sphinx site through Read the Docs after regular PyPI publication is
  established.

## Later Opportunities

- Declare a stable 1.0 API after consumer evidence supports it.
- Define stable-line support and deprecation windows before 1.0.
- Evaluate whether adjacent concerns such as contact APIs or deployment workflow helpers warrant
  separate packages or examples; keep them out of the core construct by default.
- Update `cookiecutter-aws-website` to consume this package once integration is proven stable.
- Add capabilities such as WAF or monitoring only when optional, composable, and cost-transparent.

## Completed Foundations

- Independent Python package and `src/` layout with typed public exports.
- Secure S3 and CloudFront architecture with tested defaults and configuration validation.
- Focused examples for generated hostname, external DNS, Route 53, access logs, external content,
  custom CSP, and disposable deployment.
- Layered unit, integration, end-to-end, and meta testing.
- Ruff, strict mypy, pytest coverage, pre-commit, dependency-boundary checks, strict Sphinx builds,
  artifact validation, SBOM generation, and full-SHA GitHub Action pinning.
- GitFlow routing, release policy, changelog validation, tagged GitHub Release automation, and
  maintainer runbooks.
- Public security, support, contribution, cost, configuration, testing, and deployment-test guides.

## Historical Context

This package began as the reusable delivery layer extracted from the `dagitali.com` application.
The [construct extraction history] records the completed scaffold, boundary decisions, original
consumer-adoption plan, and relationship to `cookiecutter-aws-website`. It is an architectural
record, not a second roadmap. Current priorities and status belong only in this file.

[construct-adoption playbook]: docs/playbooks/adopt-static-site-construct.md
[construct extraction history]: docs/architecture/construct-extraction-history.md
