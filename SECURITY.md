# Security Policy

- [Supported Versions](#supported-versions)
- [Reporting a Vulnerability](#reporting-a-vulnerability)
- [What to Include](#what-to-include)
- [Response Expectations](#response-expectations)

## Supported Versions

Before a stable `v1.0.0` release, security fixes are applied to the latest released version when
practical. After stable releases begin, the supported-version policy will be maintained in [support
policy].

## Reporting a Vulnerability

Report suspected vulnerabilities privately through the repository's
[GitHub private vulnerability reporting][private-reporting] feature. Do not open a public issue or
pull request containing exploit details, credentials, account identifiers, or other sensitive data.

If private vulnerability reporting is unavailable, email `security@dagitali.com` with a link to the
repository and a concise description. Do not send secrets that are unnecessary to reproduce the
issue.

## What to Include

Provide the affected version or commit, impact, reproduction steps, and any suggested mitigation.
Redact credentials and private infrastructure details from logs and screenshots.

## Response Expectations

The project is maintained on a best-effort basis. Maintainers aim to acknowledge a complete report
within three business days, investigate it privately, and coordinate disclosure after a correction
or mitigation is available. These targets are not a service-level agreement.

[private-reporting]: https://github.com/Dagitali/aws-cdk-static-site/security/advisories/new
[support policy]: SUPPORT.md
