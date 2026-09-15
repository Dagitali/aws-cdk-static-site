# Release Notes Template

Use this template when preparing a versioned document under `docs/releases/`. Keep the sections that
apply to the release, replace instructional text, and add more focused sections when the release
needs them. The committed document should explain the released behavior without depending on private
operational evidence.

- [Highlights](#highlights)
- [Change Scope](#change-scope)
- [Compatibility and Configuration](#compatibility-and-configuration)
- [Support Boundary](#support-boundary)
- [Validation](#validation)
- [Deployment and Rollback](#deployment-and-rollback)
- [Known Limitations and Follow-Up](#known-limitations-and-follow-up)

## Highlights

- Summarize the most important user-visible or operational changes.
- Explain the outcome and its value rather than listing commits or internal implementation details.
- Identify security, reliability, accessibility, or maintainability improvements when material.

## Change Scope

- Describe the package, infrastructure, automation, dependencies, or documentation affected.
- State important areas intentionally left unchanged, especially when that distinction informs
  compatibility or deployment risk.
- Link relevant pull requests, issues, architecture decisions, or public documentation by reference.

## Compatibility and Configuration

- Identify breaking behavior, deprecations, migrations, dependency constraints, or configuration
  changes.
- Record any required maintainer or consumer action.
- Write `No compatibility or configuration changes.` when none apply.

## Support Boundary

- Record release-specific changes to supported runtimes, services, regions, interfaces, or operating
  assumptions.
- Distinguish stable public behavior from internal implementation details when that affects future
  maintenance or compatibility.
- Write `No support-boundary changes.` when none apply.

## Validation

- List checks completed against the exact release candidate.
- Include relevant automated tests, static checks, synthesis or build results, artifact inspection,
  and representative manual verification.
- Distinguish completed evidence from checks that must still pass during release or deployment.

## Deployment and Rollback

- Explain whether merging or tagging triggers deployment or publication and which protected
  environment, if any, is used.
- Describe expected package, infrastructure, dependency, or operational effects.
- State whether resource replacements, data migrations, publication changes, or service interruption
  are expected.
- Provide a safe rollback or forward-fix approach appropriate to the release.

## Known Limitations and Follow-Up

- Record intentional limitations, deferred work, and monitoring expectations.
- Link public follow-up issues when available.
- Write `None.` when no release-specific limitations or follow-up work remain.

Before committing the release document, remove unused guidance, verify links and version numbers,
and ensure credentials, private identifiers, and confidential evidence are absent.
