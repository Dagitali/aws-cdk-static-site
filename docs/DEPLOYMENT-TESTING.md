# Disposable AWS Deployment Testing

The manual deployment test verifies that a synthesized construct can be created and removed in AWS
without using a production website, domain, certificate, or content bundle. It is intentionally
separate from normal CI and must remain manually triggered.

- [Bounded Resource Contract](#bounded-resource-contract)
- [Repository Configuration](#repository-configuration)
- [AWS Identity Boundary](#aws-identity-boundary)
- [Run the Test](#run-the-test)
- [Verify Cleanup](#verify-cleanup)

## Bounded Resource Contract

The workflow synthesizes [`examples/disposable-deployment/app.py`](../examples/disposable-deployment/app.py)
and rejects the template unless it contains exactly one S3 bucket, one CloudFront distribution, and
one CloudFront Origin Access Control. A response-headers policy and the bucket policy are supporting
resources on the allowlist.

The test creates no Route 53 records, ACM certificates, WAF web ACLs, access-log buckets, Lambda
functions, or deployed site content. Its S3 bucket is empty, unversioned, and assigned a delete
removal policy. Its distribution uses `PriceClass_100`. Every stack name contains the unique GitHub
run ID, concurrent runs are disabled, and the cleanup step runs after both successful and failed
post-deployment checks.

CloudFront and S3 can still incur charges while the stack exists. Review current AWS pricing and
service quotas before enabling the workflow. Do not broaden the resource allowlist without a
corresponding security, cleanup, and cost review.

## Repository Configuration

Create a protected GitHub environment named `deployment-test` and configure:

- `AWS_ACCOUNT_ID`: the single AWS account permitted for the test; and
- `AWS_DEPLOY_TEST_ROLE_ARN`: the dedicated GitHub OIDC role assumed by the workflow.

Require an environment reviewer so manual dispatch is not sufficient by itself. Keep environment
secrets empty: the workflow uses short-lived OIDC credentials and does not need access keys.

## AWS Identity Boundary

The OIDC role trust policy should accept only the repository's `deployment-test` environment
subject:

```text
repo:Dagitali/aws-cdk-static-site:environment:deployment-test
```

Give the role only the CloudFormation, CloudFront, and S3 permissions required to create, inspect,
and delete this stack. Prefer a dedicated test account and constrain permissions by stack name,
resource tag, and account wherever the AWS action supports those conditions. Do not reuse the
dagitali.com production deployment role.

## Run the Test

Run **Test disposable AWS deployment** from the GitHub Actions page on `main`. Enter the exact
confirmation value:

```text
DEPLOY-AND-DESTROY
```

The workflow refuses other branches and confirmation values. It validates the synthesized resource
allowlist before calling CloudFormation, verifies the resulting stack status, and then requests
stack deletion.

## Verify Cleanup

The final job step waits for `stack-delete-complete`. If the runner is interrupted or reaches its
timeout before cleanup completes, inspect CloudFormation for the exact
`AwsCdkStaticSiteTest-<run-id>` stack and finish deletion through a reviewed operator path. Never
delete a broader name pattern or unrelated stack.
