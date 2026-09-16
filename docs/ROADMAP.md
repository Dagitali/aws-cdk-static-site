# Extraction Roadmap

- [Completed in the Initial Scaffold](#completed-in-the-initial-scaffold)
- [Phase 2: Consumer Adoption](#phase-2-consumer-adoption)
- [Phase 3: Validate Generality](#phase-3-validate-generality)
- [Phase 4: Prepare PyPI Publication](#phase-4-prepare-pypi-publication)
- [Relationship to cookiecutter-aws-website](#relationship-to-cookiecutter-aws-website)

## Completed in the Initial Scaffold

- Establish an independent Git repository and Python package.
- Extract private S3, CloudFront OAC, security headers, cache behavior, optional content deployment,
  optional access logs, and optional Route 53/ACM behavior.
- Replace Dagitali-specific names and values with a typed public configuration.
- Add CDK assertion tests, linting, type checking, distribution builds, and CI.
- Adopt the MIT License for open-source distribution.

## Phase 2: Consumer Adoption

Consumer adoption is in progress. `dagitali.com` has adopted the released construct through a pinned
package version while keeping application-specific configuration, tags, outputs, APIs, budget, and
deployment identity in its repository. That migration established reusable evidence for property
convergence, logical-ID preservation, authenticated diff review, and rollback safety.

Use the [construct-adoption playbook] for every new or existing consumer. It covers both greenfield
deployments and state-preserving migration of deployed resources.

The next planned consumer is `datasci.me` after that software project is created. Its different
domain, content, and caching requirements will provide the second-consumer evidence needed to
evaluate the generality of the current API.

## Phase 3: Validate Generality

- Integrate `datasci.me` with different domain, content, and caching needs after its repository is
  created.
- Review whether the default security policy is practical for sites using fonts, analytics, forms,
  or third-party media.
- Add extension points only in response to demonstrated consumer requirements.
- Decide whether contact APIs, budgets, and deployment workflows belong in separate packages or
  examples; do not add them to the core construct by default.
- Keep the Sphinx documentation build local and validated by CI while the package is distributed
  through GitHub release tags.

## Phase 4: Prepare PyPI Publication

- Confirm the PyPI project name immediately before release.
- Document the supported public API and compatibility policy.
- Review the locally generated API documentation as part of the public API stabilization process.
- Retain the tag-triggered checks that build the sdist and wheel, run `twine check`, install each
  distribution in a clean environment, synthesize the representative example, and publish GitHub
  Release assets.
- Configure PyPI Trusted Publishing with a protected GitHub environment.
- Publish a prerelease before declaring a stable 1.0 API.
- Configure and publish the existing Sphinx site through Read the Docs after regular PyPI
  publication is established.

## Relationship to cookiecutter-aws-website

`cookiecutter-aws-website` creates complete project repositories. This package provides the reusable
construct within those repositories. After the API proves stable, the Cookiecutter template can
depend on this package instead of maintaining its own S3 and CloudFront implementation.

[construct-adoption playbook]: playbooks/adopt-static-site-construct.md
