# Architecture Decision Records

An Architecture Decision Record (ADR) documents a durable technical decision whose context,
alternatives, and consequences matter to future maintainers. Use this directory for ADRs, name
records `NNNN-short-title.md`, and do not rewrite accepted history; supersede an older record with a
new one.

Suggested structure:

```markdown
# NNNN: Decision Title

Status: Proposed | Accepted | Superseded

## Context
## Decision
## Consequences
## Alternatives Considered
## References
```

Routine implementation detail belongs in code or [DESIGN.md](../../DESIGN.md), not in an ADR.

Accepted records:

- [0001: Use a private S3 origin with CloudFront OAC](0001-private-s3-origin-with-oac.md)
- [0002: Retain stateful buckets by default](0002-retain-stateful-buckets-by-default.md)
- [0003: Separate validation from cloud-changing automation](0003-separate-validation-from-cloud-changes.md)
