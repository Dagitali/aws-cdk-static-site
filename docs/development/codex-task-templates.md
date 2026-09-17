# Codex Task Templates

Copy a template, replace bracketed fields, and delete irrelevant lines. Keep one task focused enough
to validate and review as a coherent diff.

- [Implement or Refactor](#implement-or-refactor)
- [Architecture or API Review](#architecture-or-api-review)
- [Documentation Synchronization](#documentation-synchronization)
- [CI/CD Maintenance](#cicd-maintenance)
- [Incident Diagnosis](#incident-diagnosis)

## Implement or Refactor

```text
In this repository, [outcome]. Inspect AGENTS.md and the current working tree first.
Scope: [paths/components]. Preserve unrelated changes and public behavior outside this scope.
Constraints: [compatibility/security/lifecycle/non-goals].
Acceptance: [observable behavior and tests].
Run [focused commands] and the broadest practical local gate. Do not deploy, publish, tag,
or change protected branches. Report changed files, evidence, validation, and remaining risks.
```

## Architecture or API Review

```text
Review [proposal/surface] against the implementation, tests, examples, and current docs.
Compare [alternatives]. Evaluate compatibility, logical-ID replacement, IAM/public access,
data retention, availability, cost, migration, and rollback where applicable.
Do not edit files. Return evidence-backed findings, open questions, and a recommended decision.
```

## Documentation Synchronization

```text
Verify [claim/change] against canonical repository sources and update only affected maintained docs.
Do not edit generated output. Check relative links and run make docs-strict when Sphinx inputs or
linked public docs are affected. Report every file changed and every skipped check.
```

## CI/CD Maintenance

```text
Update [workflow behavior] while preserving least-privilege permissions, full-SHA action pins,
credential-free normal CI, and current branch-routing policy. Inspect emitted job/check names and
synchronize CI-CD-WORKFLOWS.md, branch protection guidance, and runbooks. Run workflow policy checks.
Do not dispatch workflows or mutate repository settings unless explicitly authorized.
```

## Incident Diagnosis

```text
Diagnose [failed check/release/deployment-test/package issue]. Start read-only: identify the first
meaningful failure, affected revision/artifact/stack, and blast radius. Do not rerun, delete,
publish, revoke, or change external state without explicit authorization. Provide evidence, safe
containment, recovery options, verification, and documentation follow-up.
```
