# Examples

Examples demonstrate supported composition patterns without becoming a second implementation or a
production deployment template.

- [Basic Example](#basic-example)

## Basic Example

[`basic/`](basic/) contains a minimal CDK application and static site used to exercise the public
construct API. Review its synthesized template before deployment and replace sample names, domains,
certificates, and environment values with consumer-owned configuration.

Examples may omit production concerns that belong to the consuming application, including GitHub
OIDC roles, budgets, monitoring, contact-form APIs, and organization-specific security policy. See
the [configuration guide](../docs/CONFIGURATION.md) for supported construct options.
