# /forge-audit

Run health checks across your Forge planning setup.

## This Command's Role

Coordinate focused audit agents, each checking a different
aspect of Forge health. Run all audits or select a specific
type.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks

## Usage

```
/forge-audit [type] [options]
```

### Audit Types

| Type | Description |
|------|-------------|
| (none) | Interactive: choose audit type(s) |
| `workflow` | Audit agents, commands, skills |
| `work` | Audit efforts and slices health |
| `context` | Audit `.forge-context/` accuracy |
| `all` | Run all audits |

### Options

| Option | Description |
|--------|-------------|
| `--auto` | Non-interactive: apply all fixes |

**Context-only options:**

| Option | Description |
|--------|-------------|
| `--deep` | Read source files in project (slower) |

## Behavior

### Step 1: Parse Arguments

Parse the positional type argument and any options.

If no type provided, ask:

> "Which audits do you want to run?"
> - Workflow — Check agents, commands, skills
> - Work — Check efforts and slices for staleness
> - Context — Check `.forge-context/` accuracy
> - All — Run all audits

### Step 2: Run Selected Audits

**Workflow Audit** (`workflow` or `all`):

Spawns `Workflow Auditor` agent.

Checks:
- Command to agent references
- Agent to skill references
- Documentation completeness
- Agent integration in workflows

**Work Health Audit** (`work` or `all`):

Spawns `Work Health Auditor` agent.

Checks:
- Branch health (stale branches)
- Review summaries
- Checklist progress
- Required files present
- Effort to slice linkage

**Context Audit** (`context` or `all`):

Spawns `Context Auditor` agent.

Checks:
- Product description vs actual project
- Component descriptions vs directory structure
- Team info currency
- Principles and git workflow accuracy
- Any drift between `.forge-context/context/` and
  the actual codebase

```
Use Task tool with:
- subagent_type: "Context Auditor"
- prompt: |
    ## Inputs
    - context_path: ".forge-context/context/"
    - deep_scan: {boolean from --deep}
    - auto: {boolean from --auto}
```

With `--deep`, the Context Auditor reads actual source
files to verify component descriptions, API patterns,
and technical conventions.

### Step 3: Aggregate Results

Combine reports from all audits into unified summary.

## Audit Output Locations

All audit artifacts go to `.forge-context/artifacts/`:

| Report | Filename | Producer |
|--------|----------|----------|
| Context audit | `context-audit.md` | context-auditor |
| Workflow audit | `workflow-audit.md` | workflow-auditor |
| Work health | `work-health-audit.md` | work-health-auditor |

## Examples

### Interactive
```
User: /forge-audit

Agent: Which audits do you want to run?
       - Workflow
       - Work
       - Context
       - All

User: [Selects Work]

Agent: Running work health audit...

WORK HEALTH AUDIT REPORT
========================
[Output from work-health-auditor]
```

### Specific Audit
```
User: /forge-audit context

Agent: Running context audit...

CONTEXT AUDIT REPORT
====================
[Output from context-auditor]
```

### Context with Deep Scan
```
User: /forge-audit context --deep

Agent: Running deep context audit...

CONTEXT AUDIT REPORT
====================
[Detailed output with source file analysis]
```

### All Audits
```
User: /forge-audit all

Agent: Running all audits...
       [Spawns agents in parallel]

FORGE AUDIT SUMMARY
===================
[Combined output from all audits]
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/forge-improve` | Apply retrospective improvements |
| `/forge-retro-note` | Capture a process observation |
