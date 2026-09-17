# 0002: Retain Stateful Buckets by Default

Status: Accepted

- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)
- [Alternatives Considered](#alternatives-considered)
- [References](#references)

## Context

Stack deletion or construct refactoring can otherwise remove site content or logs. Versioned,
non-empty S3 buckets also require explicit object cleanup before deletion, so a destructive-looking
removal policy does not by itself create reliable cleanup.

## Decision

Default the content bucket to `RemovalPolicy.RETAIN`, always retain the optional access-log bucket,
and keep automatic object deletion disabled. Expire noncurrent content versions after 30 days and
access-log objects after their configured retention period.

## Consequences

Deleting a stack can leave buckets that continue to incur storage cost and need an explicit owner.
The safer default protects state from accidental stack removal. Disposable consumers that choose a
different lifecycle must plan exact cleanup and verify synthesized deletion policies.

## Alternatives Considered

Automatic deletion simplifies demos but broadens destructive permissions and can erase retained
data. Unbounded retention protects history but creates avoidable long-term storage growth.

## References

- [`StaticSite` implementation](../../src/aws_cdk_static_site/construct.py)
- [Cost considerations](../COSTS.md)
- [Learnings](../../LEARNINGS.md#an-s3-bucket-remains-after-stack-deletion)
