# Security Policy

- [Supported Versions](#supported-versions)
- [Reporting a Vulnerability](#reporting-a-vulnerability)
- [What to Include](#what-to-include)
- [Response Expectations](#response-expectations)
- [Security Model](#security-model)
- [Construct Controls](#construct-controls)
- [Consumer Responsibilities](#consumer-responsibilities)
- [Deliberate Exclusions](#deliberate-exclusions)

## Supported Versions

Before a stable `v1.0.0` release, security fixes are applied to the latest released version when
practical. After stable releases begin, the supported-version policy will be maintained in [support
policy].

## Reporting a Vulnerability

Report suspected vulnerabilities privately through the repository's [GitHub private vulnerability
reporting][private-reporting] feature. Do not open a public issue or pull request containing exploit
details, credentials, account identifiers, private incident evidence, or other sensitive data.

If private vulnerability reporting is unavailable, email `security@dagitali.com` with a link to the
repository and a concise description. Do not send secrets that are unnecessary to reproduce the
issue.

## What to Include

Provide the affected version or commit, impact, reproduction steps, and any suggested mitigation.
Redact credentials, personal data, account identifiers, and private infrastructure details from logs
and screenshots.

## Response Expectations

The project is maintained on a best-effort basis. Maintainers aim to acknowledge a complete report
within three business days, investigate it privately, and coordinate disclosure after a correction
or mitigation is available. These targets are not a service-level agreement.

## Security Model

The construct serves public static content through CloudFront while keeping its S3 origin private.
It provides a secure delivery baseline, not an application-security or account-governance system.
The consuming stack remains responsible for its content, deployment identity, domains, monitoring,
organizational controls, and any application runtime. See the [architecture] and [configuration
reference] for the complete ownership and property boundaries.

## Construct Controls

- The content bucket blocks public access, enforces TLS, uses S3-managed encryption, and permits
  CloudFront origin reads through Origin Access Control rather than public website hosting.
- CloudFront redirects viewers to HTTPS and requires the TLS 1.2 (2021) security policy for custom
  domains.
- Every cache behavior receives Content Security Policy, HSTS, frame denial, MIME-sniffing,
  referrer, permissions, cross-origin opener, and legacy XSS response headers.
- The content bucket is versioned and retained by default, automatic object deletion is disabled,
  noncurrent versions expire after 30 days, and incomplete multipart uploads expire after seven
  days.
- Optional CloudFront access logs use a separate private, encrypted, TLS-only, retained bucket with
  configurable bounded object retention.
- Invalid certificate, Route 53, domain, path, cache, and logging combinations are rejected before
  resource creation.
- Repository automation keeps normal CI credential-free, pins third-party actions to immutable
  commits, and confines the optional disposable deployment to short-lived OIDC credentials and a
  separately approved workflow.

These controls are tested through property validation, synthesized-resource assertions, examples,
and the optional `cdk-nag` AWS Solutions baseline. They are not a certification or a substitute for
reviewing the synthesized template in its consuming environment.

## Consumer Responsibilities

Consumers must review and own:

- CSP allowances and the security implications of all site content and third-party origins;
- WAF, geographic restrictions, monitoring, alerting, budgets, backup, and organizational
  guardrails;
- DNS, certificate, domain, and email/service-record safety when using custom names;
- The privacy, retention, access, and cost implications of enabling CloudFront access logs;
- Deployment permissions, artifact provenance, account and region selection, and production
  rollback; and
- Logical-ID stability, retained data, replacement risk, and `cdk diff` before deployment-sensitive
  changes.

## Deliberate Exclusions

- WAF and geographic restrictions remain consumer-owned risk, availability, and cost decisions.
- S3 server access logging is outside this delivery construct; CloudFront access logging is opt-in.
- Application APIs, authentication, secret management, budgets, monitoring, and account-wide
  controls are outside the reusable construct boundary.
- Retained buckets are not emptied automatically. Consumers choosing destructive lifecycle behavior
  need a separately reviewed emptying and recovery strategy.

[architecture]: ARCHITECTURE.md
[configuration reference]: docs/CONFIGURATION.md
[private-reporting]: https://github.com/Dagitali/aws-cdk-static-site/security/advisories/new
[support policy]: SUPPORT.md
