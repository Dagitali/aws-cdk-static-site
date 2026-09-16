# Scaffold a Consumer Project

Use this playbook to create the smallest reviewable CDK application that consumes this package. It
does not prescribe an organization-wide repository template or authorize deployment.

- [Define Ownership](#define-ownership)
- [Choose the Smallest Example](#choose-the-smallest-example)
- [Create the Baseline](#create-the-baseline)
- [Validate Without Deploying](#validate-without-deploying)
- [Production Readiness](#production-readiness)

## Define Ownership

Before generating files, record the consumer's account/region selection, stack naming, domain and
certificate model, content build and upload owner, monitoring, budgets, deployment identity, and
rollback owner. Those concerns stay in the consumer repository. The package supplies only the
reusable static-site delivery construct.

## Choose the Smallest Example

Start from one focused example: generated CloudFront hostname, external DNS, Route 53-managed DNS,
external content, access logging, or custom CSP. Copy the composition, not placeholder account IDs,
ARNs, hosted-zone IDs, domains, or a disposable-deployment stack.

## Create the Baseline

- Pin an immutable released revision of `aws-cdk-static-site`.
- Create a consumer-owned CDK app and stack with explicit environment selection where required.
- Keep configuration in typed application code or the consumer's established configuration layer.
- Add deterministic synthesis tests for selected properties and resource boundaries.
- Add local commands for format, lint, typecheck, test, and synth using the consumer's toolchain.
- Document deployment, DNS, monitoring, cost, and incident ownership before production use.

## Validate Without Deploying

Install from the pinned source, synthesize into a disposable local output directory, and inspect the
template. Check public access, OAC, TLS/certificate region, aliases, cache behavior, deletion and
update-replace policies, custom resources, and IAM. Synthesis does not prove deployed compatibility;
an existing stack also needs drift review and authenticated `cdk diff` through the consumer's
approved identity.

## Production Readiness

Before deployment, require reviewed short-lived credentials, an environment-specific change review,
site smoke tests, monitoring and budget decisions, explicit retained-resource ownership, and a
rollback plan. Use the [adoption playbook] for an existing deployment because construct-tree changes
can replace resources even when properties match.

[adoption playbook]: adopt-static-site-construct.md
