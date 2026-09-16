# Roadmap

This root roadmap summarizes current project status and links to the more detailed [extraction
roadmap](docs/ROADMAP.md). It reflects repository evidence as of the current pre-1.0 development
line; it is not a promise of dates.

- [Current State](#current-state)
- [Near Term](#near-term)
- [Before PyPI](#before-pypi)
- [Later Opportunities](#later-opportunities)
- [Completed Foundations](#completed-foundations)

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
- Convert demonstrated consumer needs into small, optional extension points rather than speculative
  framework features.

## Before PyPI

- Recheck package-name availability immediately before publication.
- Review and document the supported public API and compatibility commitments.
- Complete first- and second-consumer validation and resolve discovered ergonomics gaps.
- Configure PyPI Trusted Publishing through a protected GitHub environment; do not introduce
  long-lived credentials or manual uploads.
- Publish a prerelease and validate installation, metadata, wheel, sdist, checksums, SBOM, and basic
  synthesis from the published artifact.
- Decide when the CI-validated Sphinx site should be published through Read the Docs.

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

[construct-adoption playbook]: docs/playbooks/adopt-static-site-construct.md
