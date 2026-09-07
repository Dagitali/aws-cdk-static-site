# AGENTS

These instructions apply to automated coding agents working in this repository. User and
system-level instructions take precedence.

- [Repository Boundaries](#repository-boundaries)
- [Development Policy](#development-policy)
- [Release Readiness](#release-readiness)
- [Infrastructure Safety](#infrastructure-safety)

## Repository Boundaries

- Treat `pyproject.toml` as the canonical source for package metadata and Python-tool configuration.
- Derive package versions from Git tags through `setuptools-scm`; do not add a second version
  source.
- Preserve the `src/` package layout and the intentional exports in the package root's `__all__`.
- Keep reusable construct behavior separate from consumer-owned CDK app configuration, website
  content, deployment identity, monitoring, and account-wide controls.
- Preserve unrelated working-tree changes and generated or user-owned files.

## Development Policy

- Use Python 3.13 or newer and retain the repository's minimum-version policy checks.
- Add or update tests for changed public behavior, validation, and synthesized infrastructure.
- Keep unit tests deterministic and independent of AWS credentials, deployed resources, and network
  access.
- Run the narrowest relevant checks while iterating and `make check` before completing a change when
  practical.
- Update public documentation and `CHANGELOG.md` when user-visible behavior changes.
- Keep remote GitHub Actions pinned to full commit SHAs.

## Release Readiness

For changes affecting packaging, releases, compatibility, versioned documentation, or CI/CD, consult
[RELEASE-POLICY.md] and [RELEASE-CHECKLIST.md].

Preserve these release safeguards unless the user explicitly changes the policy:

- build both the source distribution and wheel;
- validate distributions with `twine check`;
- smoke-test the built wheel in a clean environment;
- create annotated release tags on authoritative commits merged into `main`; and
- publish through reviewed automation and trusted identity rather than long-lived credentials.

The project is not yet published to PyPI. Do not publish artifacts or configure external release
credentials unless the user explicitly authorizes that work.

## Infrastructure Safety

- Synthesize and inspect CloudFormation before proposing deployment-sensitive changes.
- Do not deploy, destroy, or modify AWS resources unless the user explicitly requests the external
  operation.
- Do not expose AWS account identifiers, credentials, private domain data, or synthesized templates
  containing sensitive values.
- Document resource replacement, security, availability, and cost implications when construct
  behavior changes.

[RELEASE-CHECKLIST.md]: RELEASE-CHECKLIST.md
[RELEASE-POLICY.md]: RELEASE-POLICY.md
