# Construct Extraction History

This document preserves the completed origin and extraction phases of `aws-cdk-static-site`. It is
an architectural history, not an active roadmap. Current priorities, sequencing, and status are
maintained only in the project [roadmap].

- [Origin](#origin)
- [Initial Extraction](#initial-extraction)
- [Consumer Adoption Milestone](#consumer-adoption-milestone)
- [Original Follow-On Intent](#original-follow-on-intent)
- [Relationship to cookiecutter-aws-website](#relationship-to-cookiecutter-aws-website)

## Origin

The reusable construct originated in the `dagitali.com` application. The extraction separated its
general static-site delivery layer from application-specific configuration, APIs, tags, outputs,
budgets, monitoring, content, and deployment identity.

The intended package boundary was a secure, cost-conscious Python AWS CDK construct rather than a
complete website application or deployment template.

## Initial Extraction

The initial scaffold:

- Established an independent Git repository and Python package;
- Extracted private S3 storage, CloudFront Origin Access Control, security headers, cache behavior,
  optional content deployment, optional access logs, and optional Route 53 and ACM behavior;
- Replaced Dagitali-specific names and values with typed public configuration;
- Added CDK assertion tests, linting, strict type checking, distribution builds, documentation, and
  continuous integration; and
- Adopted the MIT License for open-source distribution.

This phase established the public `StaticSite` and `StaticSiteProps` boundary while deliberately
leaving consumer-owned concerns outside the package.

## Consumer Adoption Milestone

`dagitali.com` became the first consumer through a pinned package release. Its migration retained
application-specific configuration, tags, outputs, APIs, budget, and GitHub OIDC deployment workflow
in the consumer repository.

The adoption demonstrated that moving deployed resources beneath a reusable construct requires more
than equivalent properties. The consumer first converged resource properties, then preserved
deployed CloudFormation logical IDs during the source refactor, protected those identities with
regression tests, and required an authenticated zero-difference CDK review before deployment.

Those reusable operational lessons now live in the [construct-adoption playbook]. The playbook, not
this historical record, governs future consumer adoption.

## Original Follow-On Intent

The extraction plan anticipated:

- Validation with a second static website having different domain, content, and caching needs;
- Review of the default security policy against fonts, analytics, forms, and third-party media;
- Extension points driven by demonstrated consumer requirements rather than speculation;
- Continued separation of contact APIs, budgets, and deployment workflows from the core construct;
- Public API and compatibility review before PyPI publication;
- Trusted publishing, prerelease validation, and retention of wheel, sdist, checksum, SBOM, clean
  installation, synthesis, and GitHub Release checks; and
- Read the Docs publication after a regular PyPI lifecycle was established.

These items are preserved here as the extraction's original direction. Their current status and
priority are maintained in the active [roadmap].

## Relationship to cookiecutter-aws-website

`cookiecutter-aws-website` creates complete project repositories. This package supplies the reusable
construct that those repositories can compose. The extraction intentionally kept project scaffolding
and reusable AWS infrastructure as separate responsibilities.

[construct-adoption playbook]: ../playbooks/adopt-static-site-construct.md
[roadmap]: ../../ROADMAP.md
