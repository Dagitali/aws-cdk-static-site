# Architecture Decision Records

An Architecture Decision Record (ADR) documents a durable technical decision whose context,
alternatives, and consequences matter to future maintainers. ADRs complement current-state
documentation; if a record conflicts with running code or tests, investigate and reconcile both
rather than silently trusting either source.

| ADR | Status | Decision |
| --- | --- | --- |
| [0001](0001-private-s3-origin-with-oac.md) | Accepted | Use a private S3 origin with CloudFront OAC |
| [0002](0002-retain-stateful-buckets-by-default.md) | Accepted | Retain stateful buckets by default |
| [0003](0003-separate-validation-from-cloud-changes.md) | Accepted | Separate validation from cloud-changing automation |

## Adding a Decision

Name records `NNNN-short-title.md` and copy this structure into the next zero-padded file:

```markdown
# NNNN: Decision Title

- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Supersedes: ADR NNNN, if applicable

## Context
## Decision
## Consequences
## Alternatives Considered
## Verification
## References
```

Use the date the decision is accepted or reconstructed from repository evidence. Do not rewrite
accepted history to make an old decision appear current; add a new record that explicitly supersedes
it. Routine implementation detail belongs in code or [DESIGN.md](../../DESIGN.md), not in an ADR.
