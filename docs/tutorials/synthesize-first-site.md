# Synthesize a First Static Site

This tutorial proves the smallest package composition locally. It does not deploy AWS resources. Use
Python 3.13 or 3.14 and a clean virtual environment.

- [Install the Checkout](#install-the-checkout)
- [Choose the Generated-Hostname Example](#choose-the-generated-hostname-example)
- [Inspect the Result](#inspect-the-result)
- [Choose the Next Composition](#choose-the-next-composition)

## Install the Checkout

From the repository root:

```bash
python -m pip install -e '.[dev]'
```

For a real consumer repository, replace the editable checkout with an immutable release tag as shown
in the root README.

## Choose the Generated-Hostname Example

`examples/cloudfront-domain/app.py` needs no custom certificate or hosted zone. Read the example,
then synthesize it:

```bash
CDK_OUTDIR=cdk.out python examples/cloudfront-domain/app.py
```

This creates a local cloud assembly. It does not contact AWS or create resources.

## Inspect the Result

In the synthesized template, verify that the origin bucket blocks public access, CloudFront uses an
Origin Access Control, viewers redirect to HTTPS, and retained state matches the project's lifecycle
policy. Do not treat generated logical IDs as a stable public API.

Run the maintained example test for repeatable verification:

```bash
make test-examples
```

## Choose the Next Composition

Use `examples/external-dns/` when another provider owns DNS and an existing `us-east-1` certificate
is supplied. Use `examples/route53-managed/` when the consumer supplies a Route 53 hosted zone and
intentionally creates aliases and a DNS-validated certificate. Use `examples/external-content/` when
a separate pipeline owns upload and invalidation.

Before any deployment, replace documentation-only identifiers, review costs and retained resources,
bootstrap the consumer account, run an authenticated `cdk diff`, and use the consumer's approved
short-lived deployment identity.
