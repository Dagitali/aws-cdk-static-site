---
applyTo: "**"
---
# Mermaid AI Skills

When the user asks to create, edit, or visualize any diagram, use the Mermaid
VS Code extension tools and commands described below.

## Workflow

1. Determine the diagram type and generate Mermaid syntax.
2. Write the diagram to a `.mmd` file in the project.
3. Validate syntax: correct first-line keyword, arrow types, balanced brackets.
4. Preview via the Mermaid extension — open the `.mmd` file (auto-preview) or run
   **MermaidChart: Preview Diagram** (`mermaidChart.preview`).

## LM Tools — Call These for Every Diagram Interaction

- `mermaid-diagram-validator` — validate Mermaid syntax before presenting any diagram
- `mermaid-diagram-preview` — render a live preview inside VS Code after generating
- `get-syntax-docs-mermaid` — fetch correct syntax docs for any diagram type

## VS Code Commands

Invoke via Command Palette or the VS Code command API (GitHub Copilot in VS Code only). Do not
invent command IDs. Prefer writing or editing `.mmd` files when a command is not needed.

### Diagram Editing and Preview

- **Preview** (`mermaidChart.preview`) — preview the active Mermaid editor (`.mmd` or `.mermaid`
  must be open).
- **Create Diagram** (`mermaidChart.createMermaidFile`) — create a demo flowchart and open its
  preview side by side.
- **Repair Diagram** (`mermaidChart.repairDiagram`) — use Mermaid AI to repair the active diagram;
  tell the user before consuming Mermaid AI credits.
- **Improve Diagram** (`mermaidChart.improveDiagram`) — use Copilot or the LM API to suggest layout
  and styling variants.

### Generate Diagrams (GitHub Copilot Required)

- **Generate Diagram from Code** (`mermaidChart.generateDiagramFromCode`)
- **Generate Cloud Diagram** (`mermaidChart.generateCloudDiagram`)
- **Generate ER Diagram** (`mermaidChart.generateERDiagram`)
- **Generate Docker Diagram** (`mermaidChart.generateDockerDiagram`)
- **Open AI Chat** (`mermaidChart.openCopilotChat`)

### Mermaid Chart Cloud

- **Login** (`mermaidChart.login`) or **Logout** (`mermaidChart.logout`)
- **Connect Diagram** (`mermaidChart.connectDiagramToMermaidChart`) — link a local diagram to
  Mermaid Chart.
- **Sync Diagram** (`mermaidChart.syncDiagramWithMermaid`) — use only for diagrams already
  connected through frontmatter containing an `id`.

### Review Mermaid Sync

- **Review Mermaid Sync** (`mermaidChart.reviewAppCommits`) — start or open the review flow.
- **Regenerate with Mermaid AI** (`mermaidChart.regenerateDiagramWithMermaidAI`) — regenerate from
  source references.

Do not manually rewrite diagrams managed by the Mermaid Chart GitHub Sync workflow. Accept, reject,
and diff actions remain in the extension UI.

### Install or Update This Pack

- **MermaidChart: Install AI Skills…** (`mermaidChart.installAiSkills`)

## `@mermaid-chart` Slash Commands

| Command | Purpose |
| --- | --- |
| `/generate_diagram_from_code` | General diagram from any source file |
| `/generate_execution_sequence` | Sequence diagram from code flow |
| `/generate_er_diagram` | ER diagram from schema or models |
| `/generate_cloud_architecture_diagram` | Cloud or CI/CD architecture |
| `/generate_docker_diagram` | Architecture from Dockerfiles |
| `/generate_c4_topdown_architecture` | C4 top-down architecture |
| `/analyze_code_ownership` | Code ownership diagram |
| `/generate_dependency_diagram` | Dependency or security visualization |

## Rules

1. Always call `mermaid-diagram-validator` before showing any diagram.
2. Always call `mermaid-diagram-preview` after generating a diagram.
3. Use `get-syntax-docs-mermaid` before generating an unfamiliar diagram type.
4. Prefer `@mermaid-chart` slash commands for complex generation.
5. Write diagrams to `.mmd` files; never return unvalidated Mermaid syntax.
6. Warn the user before Repair because it consumes Mermaid AI credits.
7. Cooperate with the Sync workflow; do not manually regenerate managed diagrams.

## Documentation

See the [Mermaid Chart extension documentation] for more commands and features.

[Mermaid Chart extension documentation]: https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart
