# Forge Plugin

**F**ramework for **O**rganized **R**equirements & **G**uided **E**ngineering

A Claude Code plugin that brings structured planning workflows
to any engineering team. Forge guides discovery, requirements,
design, and implementation — producing markdown artifacts that
live alongside your code.

## What Forge Provides

- **Effort discovery** — Explore problem spaces before committing
  to solutions
- **Slice delivery** — Break work into focused, shippable slices
  with requirements and design
- **Implementation discipline** — TDD, systematic debugging, and
  verification-before-complete built into every workflow
- **Retro-driven improvement** — Capture corrections as retro
  notes; apply them to improve your own guidelines and templates
- **Self-contained** — All planning artifacts live in
  `.forge-context/` in your project repo, committed with your code

## Installation

Install via the Claude Code plugin marketplace:

```bash
claude plugin add-marketplace https://github.com/flox/forge-plugin
claude plugin install forge
```

## Quick Start

Initialize Forge in your project:

```
/forge-init
```

This scaffolds `.forge-context/` in your project with starter
templates for efforts, slices, and team context.

Then start an effort to explore a new problem:

```
/forge-explore
```

Or jump straight into a delivery slice:

```
/forge-work
```

## Commands

| Command | Purpose |
|---------|---------|
| `/forge-init` | Initialize Forge in your project |
| `/forge-explore` | Discover and understand problem spaces |
| `/forge-work` | Build and deliver focused slices |
| `/forge-requirements` | Run requirements gathering |
| `/forge-design` | Run the design phase |
| `/forge-implement` | Ad-hoc changes without slice ceremony |
| `/forge-investigate` | Investigate bugs and issues |
| `/forge-start-task` | Start work on implementation tasks |
| `/forge-retro-note` | Capture a process observation |
| `/forge-improve` | Apply retro notes as improvements |
| `/forge-phase-complete` | Complete a slice phase |
| `/forge-audit` | Health checks on work and context |
| `/forge-digest` | Activity digest |
| `/forge-reviewable` | Restructure commits for review |
| `/forge-process-pr-discussions` | Process PR discussions |

## Documentation

- [Getting Started](docs/getting-started.md)
- [Workflow Overview](docs/workflow-overview.md)
- [Command Reference](docs/command-reference.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0. See [LICENSE](LICENSE).
