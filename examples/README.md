# Examples

Examples demonstrate supported composition patterns without becoming a second implementation or a
production deployment template.

- [Basic Example](#basic-example)
- [Run the Example](#run-the-example)

## Basic Example

[`basic/`](basic/) contains a minimal CDK application and static site used to exercise the public
construct API. Review its synthesized template before deployment and replace sample names, domains,
certificates, and environment values with consumer-owned configuration.

## Run the Example

From the repository root, install the package and synthesize the example stack:

```bash
python -m pip install -e .
CDK_OUTDIR=cdk.out python examples/basic/app.py
```

The second command uses POSIX shell syntax to retain the generated assembly under `cdk.out/`;
synthesis does not deploy resources. Inspect the generated CloudFormation before using `cdk deploy`
in a bootstrapped, consumer-owned AWS account.

Examples may omit production concerns that belong to the consuming application, including GitHub
OIDC roles, budgets, monitoring, contact-form APIs, and organization-specific security policy. See
the [configuration guide](../docs/CONFIGURATION.md) for supported construct options.
