# Cost Considerations

The construct favors low-cost defaults, but it does not make AWS usage free or create an
account-level budget. Actual charges depend on region, traffic, object count and size,
invalidations, logging, and AWS pricing changes.

- [Resources That Can Incur Charges](#resources-that-can-incur-charges)
- [Important Behaviors](#important-behaviors)
- [Consumer Responsibilities](#consumer-responsibilities)

## Resources That Can Incur Charges

| Resource | Cost drivers | Default safeguard |
| --- | --- | --- |
| S3 content bucket | Stored bytes, requests, versioned objects, and data transfer | S3-managed encryption and expiration of noncurrent versions after 30 days |
| CloudFront | Requests, data transfer, functions if later added, and excess invalidation paths | `PriceClass_100`, compressed responses, and optimized asset caching |
| Bucket deployment | Lambda execution, staging assets, S3 requests, logs, and invalidation | Created only when `site_content_path` is supplied; 512 MB memory and one-week logs |
| Access-log bucket | Log delivery requests and retained log objects | Disabled by default with configurable retention when enabled |
| Route 53 | Hosted zones and DNS queries | Records are created only when explicitly requested in an existing zone |
| ACM public certificate | Certificate issuance is generally not the principal cost, but associated services remain billable | Created only when explicitly requested |

## Important Behaviors

- `RemovalPolicy.RETAIN` protects the content bucket from accidental deletion but can leave billable
  storage after a stack is removed.
- Versioning improves recoverability but retains replaced objects until the 30-day
  noncurrent-version lifecycle rule expires them.
- CloudFront invalidations use `/*` after an integrated content deployment. Review current free
  allowances and pricing before increasing deployment frequency substantially.
- Disabling access logs avoids their storage and request costs but reduces operational evidence.
- `PriceClass_100` reduces edge coverage as well as cost; applications needing broader geographic
  performance can select another price class deliberately.

## Consumer Responsibilities

The consuming application should establish budgets and alerts at the appropriate account, project,
or tag boundary. An account-wide budget is intentionally outside this construct because a reusable
site component cannot safely assume ownership of all account spending.

Before production deployment, review the [AWS Pricing Calculator], [Amazon S3 pricing], [Amazon
CloudFront pricing], and [Route 53 pricing]. Recheck pricing when traffic patterns or enabled
features change.

[Amazon CloudFront pricing]: https://aws.amazon.com/cloudfront/pricing/
[Amazon S3 pricing]: https://aws.amazon.com/s3/pricing/
[AWS Pricing Calculator]: https://calculator.aws/
[Route 53 pricing]: https://aws.amazon.com/route53/pricing/
