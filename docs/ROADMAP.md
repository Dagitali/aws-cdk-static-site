# Extraction Roadmap

- [Completed in the Initial Scaffold](#completed-in-the-initial-scaffold)
- [Phase 2: Integrate the First Consumer](#phase-2-integrate-the-first-consumer)
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

## Phase 2: Integrate the First Consumer

1. Add this repository to `dagitali.com` as a Git-pinned dependency.
2. Refactor `DagitaliSiteStack` to compose `StaticSite` while retaining its application-specific
   configuration, tags, outputs, contact form, and budget.
3. Compare the synthesized CloudFormation template before and after migration.
4. Deploy to a non-production stack and run the public-site checks.
5. Deploy production through the existing GitHub OIDC workflow.

The Git dependency should remain pinned to a full commit SHA until this package
has stable releases.

## Phase 3: Validate Generality

- Integrate a second static website with different domain and caching needs.
- Review whether the default security policy is practical for sites using fonts, analytics, forms,
  or third-party media.
- Add extension points only in response to demonstrated consumer requirements.
- Decide whether contact APIs, budgets, and deployment workflows belong in separate packages or
  examples; do not add them to the core construct by default.

## Phase 4: Prepare PyPI Publication

- Confirm the PyPI project name immediately before release.
- Document the supported public API and compatibility policy.
- Generate API documentation.
- Retain the tag-triggered checks that build the sdist and wheel, run `twine check`, install each
  distribution in a clean environment, synthesize the representative example, and publish GitHub
  Release assets.
- Configure PyPI Trusted Publishing with a protected GitHub environment.
- Publish a prerelease before declaring a stable 1.0 API.

## Relationship to cookiecutter-aws-website

`cookiecutter-aws-website` creates complete project repositories. This package provides the reusable
construct within those repositories. After the API proves stable, the Cookiecutter template can
depend on this package instead of maintaining its own S3 and CloudFront implementation.
