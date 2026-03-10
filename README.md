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

Three commands to get going:

```
/forge-init
```

Analyzes your project and scaffolds `.forge-context/` with
starter templates and context.

```
/forge-explore
```

Start an effort to explore a problem space and identify
what to build.

```
/forge-work new
```

Start a delivery slice once you know what to build.

## What's Included

| Type | Count | Purpose |
|------|-------|---------|
| Commands | 15 | Slash commands for the full workflow |
| Agents | 18 | Subagents for requirements, design, review, and more |
| Skills | 21 | Reusable knowledge modules |
| Templates | 11 | Scaffold templates copied to your project |

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

- [Getting Started](docs/getting-started.md) — Installation
  walkthrough and first effort/slice
- [Workflow Overview](docs/workflow-overview.md) — How efforts
  and slices work
- [Command Reference](docs/command-reference.md) — All commands
  with descriptions and arguments

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add commands,
agents, and skills.

## License

Apache 2.0. See [LICENSE](LICENSE).
