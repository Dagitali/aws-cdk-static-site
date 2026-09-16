# Public API Evolution Checklist

Use this checklist for changes to `StaticSite`, `StaticSiteProps`, package-root exports, defaults,
validation, or synthesized behavior. The public contract includes Python types and errors as well as
the CloudFormation resources consumers receive.

- [Establish the Contract](#establish-the-contract)
- [Implement and Prove](#implement-and-prove)
- [Synchronize Documentation](#synchronize-documentation)
- [Validate and Report](#validate-and-report)

## Establish the Contract

- Identify a demonstrated consumer or correctness requirement.
- Decide whether the change is additive, behavior-changing, deprecating, or breaking under the
  [release policy].
- Choose a safe default and list invalid combinations before implementation.
- Record an ADR when the choice establishes a cross-cutting security, lifecycle, or ownership rule.

## Implement and Prove

- Update typed public docstrings and intentional exports in `src/aws_cdk_static_site/__init__.py`.
- Validate inputs before resource creation.
- Add focused property-validation and synthesized-resource tests.
- Preserve stateful construct IDs unless a separately reviewed migration permits replacement.
- Add or update the smallest example that proves the supported composition.

## Synchronize Documentation

Review `docs/CONFIGURATION.md`, `ARCHITECTURE.md`, `DESIGN.md`, `docs/COSTS.md`, the Sphinx API
source, examples, and `CHANGELOG.md`. Update only the documents whose claims changed. Follow the
[documentation synchronization guide] rather than copying API text into a second reference.

## Validate and Report

Run `make lint typecheck test-unit test-integration`, then the broader gate appropriate to the
change. Inspect synthesized templates for replacement, IAM, custom-resource, security, availability,
and cost impact. Report any intentionally deferred consumer migration or release work.

[documentation synchronization guide]: ../development/documentation-sync.md
[release policy]: ../../RELEASE-POLICY.md
