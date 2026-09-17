# Adopt the Static Site Construct

Use this playbook to replace consumer-owned static-site delivery resources with the reusable
`aws-cdk-static-site` construct, or to introduce the construct into a new consumer application. It
keeps application-specific responsibilities in the consumer and makes infrastructure identity,
security, availability, and cost changes explicit. Review the package [architecture], [design], and
[testing guide] before planning a production migration.

- [Outcomes](#outcomes)
- [Choose the Adoption Path](#choose-the-adoption-path)
- [Prepare the Consumer](#prepare-the-consumer)
- [Capture the Existing Baseline](#capture-the-existing-baseline)
- [Converge Resource Properties](#converge-resource-properties)
- [Integrate the Construct](#integrate-the-construct)
- [Validate the Candidate](#validate-the-candidate)
- [Deploy and Verify](#deploy-and-verify)
- [Retain Migration Safeguards](#retain-migration-safeguards)
- [Feed Evidence Back to the Library](#feed-evidence-back-to-the-library)

## Outcomes

A completed adoption should:

- Use an immutable package revision;
- Compose `StaticSite` and `StaticSiteProps` from a consumer-owned stack;
- Leave site configuration, tags, outputs, APIs, budgets, monitoring, and deployment identity in the
  consumer;
- Preserve deployed resources unless replacement was separately planned and approved;
- Pass the consumer's full validation suite and an authenticated CDK diff;
- Deploy through the consumer's reviewed, short-lived AWS identity; and
- Record consumer requirements without coupling the library to one site.

## Choose the Adoption Path

Use the **new deployment** path when the consumer has no deployed static-site resources. Review the
entire synthesized template as a new resource set, deploy first to a non-production environment, and
verify cleanup and cost boundaries before production.

Use the **existing deployment** path when S3, CloudFront, Route 53, ACM, access logging, or content
deployment resources already exist. Treat this as a state-preserving migration. Moving resources
beneath a new CDK construct changes construct paths and normally changes CloudFormation logical IDs.
An ordinary deployment can therefore interpret a source refactor as removals, replacements, and new
resources even when the intended properties are identical.

Do not combine resource-property changes, logical-ID changes, and construct-tree refactoring in one
deployment. Separating them makes each change set reviewable and gives rollback a stable baseline.

## Prepare the Consumer

1. Identify the consumer's supported Python and AWS CDK versions and confirm they overlap the
   package requirements.
2. For evaluation of unreleased source, pin the dependency to a full commit SHA. For maintained
   adoption, pin an immutable release tag. Do not depend on an adjacent checkout.
3. Install the dependency through the consumer's normal reproducible setup and update every
   canonical dependency declaration together.
4. Inventory responsibilities that must remain consumer-owned, including:

   - CDK app and environment selection;
   - Account, region, and stack naming;
   - Domain and certificate configuration;
   - Tags and CloudFormation outputs;
   - Application APIs, budgets, monitoring, analytics, and content;
   - GitHub OIDC roles and deployment workflows; and
   - Site-specific security and cache requirements.
5. Read the package [configuration reference] and select only the integrations the consumer needs.

## Capture the Existing Baseline

For an existing deployment:

1. Retrieve the deployed CloudFormation template through an approved read-only identity.
2. Complete drift detection and resolve unexplained drift before changing source.
3. Record the logical IDs, physical IDs, deletion policies, update-replace policies, and important
   properties of stateful or globally constrained resources.
4. Synthesize the current consumer source and compare it with the deployed template.
5. Run an authenticated `cdk diff` and save the result with the migration evidence.
6. Identify cross-stack exports and imports. Removing a cross-stack reference can require a staged
   two-deployment migration; do not remove producer and consumer references simultaneously.
7. Record the exact source revision, package revision, account, region, and stack name used for the
   baseline without committing private identifiers.

At minimum, protect the content bucket, bucket policy, CloudFront distribution, Origin Access
Control, response-headers policy, access-log bucket, deployment log group, and bucket-deployment
custom resources when those resources already exist.

## Converge Resource Properties

Before moving existing resources into `StaticSite`, compare their deployed properties with the
properties synthesized by the pinned package revision.

1. Change the consumer's existing flat definitions to match the target properties.
2. Deploy property-only changes separately.
3. Reject any convergence change set that unexpectedly replaces a stateful resource or distribution.
4. Verify the site after convergence and capture a new clean baseline.

Skip this phase only when the existing and target properties already match or when every difference
has been deliberately reviewed as part of a separate migration.

## Integrate the Construct

1. Import `StaticSite` and `StaticSiteProps` from the pinned package.
2. Replace only the reusable delivery resources. Keep consumer-owned responsibilities in the
   consumer stack.
3. Preserve existing construct IDs and logical IDs where an ordinary deployment must retain
   resources. Add regression tests for every compatibility override.
4. Do not remove compatibility overrides after deployment merely because adoption succeeded.
   Removing one is another identity migration.
5. Use CDK refactoring only after confirming that every affected resource type and relationship is
   supported. Custom resources can make refactor plans ineligible. Never mix a refactor operation
   with resource-property changes.
6. Keep external DNS, certificate, content, access logging, and immutable-cache choices explicit in
   `StaticSiteProps`.

## Validate the Candidate

Run validation against the exact revision proposed for integration:

1. Run the consumer's complete local quality and test suite.
2. Synthesize every affected stack.
3. Assert expected resource types and properties.
4. For existing deployments, assert that protected deployed logical IDs remain present and that
   construct-generated replacement IDs are absent.
5. Run an authenticated `cdk diff` against each deployed stack.
6. For a no-change adoption, require zero additions, removals, replacements, and property changes.
7. If changes are intentional, classify each change and document its replacement, security,
   availability, cost, and rollback effects.
8. Confirm the consumer's pull-request workflows pass for the exact commit.

Do not infer safety from a successful synthesis alone. Synthesis proves that a template can be
assembled; the authenticated diff compares it with deployed state.

## Deploy and Verify

1. Deploy to a representative non-production environment when one exists.
2. Run site checks covering DNS, TLS, redirects, expected content, error handling, security headers,
   cache behavior, logs, and application-specific integrations.
3. Review the production change set or authenticated diff again from the exact approved revision.
4. Deploy through the consumer's existing reviewed workflow using short-lived OIDC credentials.
5. Verify stack completion and confirm protected physical IDs remain unchanged.
6. Repeat the production site checks and inspect CloudFormation events for unexpected replacement or
   rollback behavior.
7. Confirm retained data, temporary assets, and failed-stack artifacts are handled according to the
   consumer's cleanup policy.

Never tear down a production stack merely to simplify construct adoption.

## Retain Migration Safeguards

- Keep logical-ID compatibility code and regression tests until a separate migration removes them.
- Preserve the last known-good source and dependency revision for rollback.
- Before rollback, run an authenticated diff against the restored source and reject unexpected
  replacement.
- Keep release tags immutable, including tags associated with failed deployments.
- Document any failed deployment and the state CloudFormation retained after rollback.

## Feed Evidence Back to the Library

After adoption:

1. Record which defaults worked and which consumer-specific overrides were necessary.
2. Add library extension points only for requirements demonstrated by more than one consumer or for
   clear correctness and security needs.
3. Keep application APIs, budgets, deployment identities, and organization-specific controls out of
   the core construct by default.
4. Update examples, configuration documentation, tests, roadmap status, and learnings when the
   adoption reveals a reusable lesson.

[architecture]: ../../ARCHITECTURE.md
[configuration reference]: ../CONFIGURATION.md
[design]: ../../DESIGN.md
[testing guide]: ../TESTING.md
