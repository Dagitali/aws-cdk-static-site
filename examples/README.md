# Examples

Examples demonstrate supported composition patterns without becoming a second implementation or a
production deployment template.

- [Available Examples](#available-examples)
- [Run the Example](#run-the-example)

## Available Examples

[`basic/`][basic example] contains a minimal CDK application and static site used to exercise the
public construct API. Review its synthesized template before deployment and replace sample names,
domains, certificates, and environment values with consumer-owned configuration.

Focused examples cover one composition decision at a time:

- [`cloudfront-domain/`][generated-hostname example] uses CloudFront's generated hostname without
  custom DNS.
- [`external-dns/`][external-DNS example] configures an external DNS provider with an imported ACM
  certificate.
- [`route53-managed/`][Route 53 example] creates Route 53 aliases and a DNS-validated ACM
  certificate.
- [`access-logging/`][access-logging example] enables access logs with bounded retention.
- [`external-content/`][external-content example] leaves content upload and invalidation to another
  deployment system.
- [`custom-csp/`][custom-CSP example] supplies a site-specific Content Security Policy.
- [`disposable-deployment/`][disposable-deployment example] synthesizes the fixed, empty resource set
  used only by the manually approved AWS deployment test.

The external-DNS and Route 53 examples use documentation-only identifiers. Replace every account ID,
certificate ARN, hosted-zone ID, and domain name before deployment. CloudFront certificates must
exist in `us-east-1`; construct-managed certificate creation also requires the stack itself to
target `us-east-1`.

## Run the Example

From the repository root, install the package and synthesize the example stack:

```bash
python -m pip install -e .
CDK_OUTDIR=cdk.out python examples/cloudfront-domain/app.py
```

The second command uses POSIX shell syntax to retain the generated assembly under `cdk.out/`;
synthesis does not deploy resources. Inspect the generated CloudFormation before using `cdk deploy`
in a bootstrapped, consumer-owned AWS account.

Examples may omit production concerns that belong to the consuming application, including GitHub
OIDC roles, budgets, monitoring, contact-form APIs, and organization-specific security policy. See
the [configuration guide] for supported construct options or build the [local Sphinx documentation]
to browse every example with generated API docs.

Do not deploy the disposable example directly. Use the guarded workflow documented in [Disposable
AWS Deployment Testing], which validates its resource allowlist and
performs cleanup.

[access-logging example]: access-logging/
[basic example]: basic/
[configuration guide]: ../docs/CONFIGURATION.md
[custom-CSP example]: custom-csp/
[disposable-deployment example]: disposable-deployment/
[Disposable AWS Deployment Testing]: ../docs/DEPLOYMENT-TESTING.md
[external-content example]: external-content/
[external-DNS example]: external-dns/
[generated-hostname example]: cloudfront-domain/
[local Sphinx documentation]: ../docs/README.md
[Route 53 example]: route53-managed/
