# Architecture Notes

Use this directory for focused component diagrams, threat models, and deeper architectural analyses.
The repository-wide baseline is [ARCHITECTURE.md](../../ARCHITECTURE.md), and design principles live
in [DESIGN.md](../../DESIGN.md).

The [construct extraction history](construct-extraction-history.md) preserves how the reusable
package was separated from its original consumer. It is historical context; the root
[roadmap](../../ROADMAP.md) is the only active project roadmap.

The [change-impact map](change-impact-map.md) connects source areas to tests, documentation, and
review risks so maintainers and agents can bound changes before editing.

New notes should identify scope, decisions, operational consequences, and related [Architecture
Decision Records (ADRs)][ADRs]. Keep consumer-specific production details outside this reusable
library repository.

[ADRs]: ../decisions/README.md
