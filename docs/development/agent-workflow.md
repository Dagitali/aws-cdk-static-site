# ChatGPT and Codex Workflow

Use ChatGPT and Codex as complementary review surfaces. ChatGPT is useful before a repository change
exists; Codex is responsible for grounding and executing work in the current checkout.

- [Use ChatGPT For](#use-chatgpt-for)
- [Use Codex For](#use-codex-for)
- [Recommended Handoff](#recommended-handoff)
- [Execution Loop](#execution-loop)

## Use ChatGPT For

- Clarifying outcomes, constraints, alternatives, and acceptance criteria;
- Architecture and API option review before choosing a direction;
- Threat, migration, operability, and cost questions that benefit from a second perspective; and
- Turning an ambiguous idea into a bounded task brief.

Do not treat a conversational recommendation as current repository fact. Versions, commands,
workflow names, resource behavior, and roadmap state must be verified in the checkout.

## Use Codex For

- Reading implementation, tests, configuration, Git history, and existing working-tree changes;
- Producing focused repository edits while preserving unrelated work;
- Running the narrowest meaningful checks and inspecting the diff; and
- Reporting changed files, evidence, validation, risks, and follow-up.

Codex must not deploy, destroy, publish, tag, change protected branches, or access secrets unless
the user explicitly authorizes that external action.

## Recommended Handoff

A useful architecture-review handoff contains:

1. Desired outcome and non-goals;
2. Relevant repository paths or public interfaces;
3. Alternatives considered and unresolved questions;
4. Compatibility, security, data, cost, and migration constraints; and
5. Acceptance criteria that can be verified locally.

Codex then validates the brief against repository evidence. If it conflicts with the checkout, Codex
should surface the conflict instead of implementing the conversation literally.

## Execution Loop

1. Inspect instructions, status, and canonical sources.
2. Bound the files and external side effects.
3. Make the smallest coherent change.
4. Run focused checks, then the broader appropriate gate.
5. Review the diff for unrelated changes and documentation drift.
6. Record durable decisions in [Architecture Decision Records (ADRs)][architecture decision records]
   and reusable failures in `LEARNINGS.md`.
7. Return an evidence-based completion report.

Use the [Codex task templates] for common change types and the [change-impact map] to find dependent
tests and documentation.

[ADRs]: ../decisions/README.md
[change-impact map]: ../architecture/change-impact-map.md
[Codex task templates]: codex-task-templates.md
