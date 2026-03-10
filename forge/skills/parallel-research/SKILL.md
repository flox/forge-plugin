---
name: parallel-research
description: >-
  This skill should be used when a command spawns an
  agent that defines a "Research Lenses" section —
  detects agent teams capability, prompts user if
  available, and executes lenses as parallel subagents
  or team teammates. Do not use for agents without a
  Research Lenses section.
---

# Parallel Research Execution

Execute an agent's Research Lenses in parallel, using agent
teams when available or parallel subagents as the default.

## When to Use

Commands reference this skill when spawning an agent that
defines a `## Research Lenses` section. The skill handles:
1. Detecting whether agent teams are enabled
2. Prompting the user if teams are available
3. Executing lenses via the chosen mode

## Detection Step

Before spawning the primary agent, check for teams capability:

```bash
echo "$CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
```

If the value is `1` or `true`, teams are available.

## Execution Modes

### Teams Available

Prompt the user with AskUserQuestion:

```
question: "This task benefits from parallel research.
  Use a team for richer analysis? Each research
  perspective can challenge and build on the others'
  findings in real-time."
options:
  - label: "Use a team (Recommended)"
    description: "Each research perspective runs as a
      teammate that can share findings and challenge
      other perspectives in real-time."
  - label: "Standard mode"
    description: "Parallel research still runs via
      subagents, but perspectives work independently
      without cross-pollination."
```

**On "Use a team":**
- Create a team with one teammate per lens
- Each teammate receives: shared context + lens prompt
- Team lead synthesizes results after all lenses complete
- Lead presents synthesis to user at the normal gate

**On "Standard mode":**
- Spawn the agent normally
- Agent internally uses parallel Task calls for each lens

### Teams Not Available

Spawn the agent normally. No prompt, no mention of teams.
The agent uses parallel Task calls (subagents) for its
Research Lenses internally.

## How Agents Define Lenses

Agents declare lenses in a `## Research Lenses` section:

```markdown
## Research Lenses

When reaching the exploration phase, spawn these as
parallel subagents. Each lens receives the shared context
inputs listed below.

### Lens: {Name}
{Self-contained research prompt}
Focus: {what to look for}
Output: {what to return}

### Lens: {Name}
...

## Lens Synthesis
After all lenses complete, merge results:
- Identify agreements (high-confidence findings)
- Flag contradictions (most valuable — investigate)
- Note gaps (what no lens covered)
```

The agent does not know or care whether it runs as a team
lead or uses subagents. It follows the same instructions
either way.

## Subagent Constraint

**Critical:** When an agent with Research Lenses is itself
spawned as a subagent (via Task), it cannot spawn its own
lens subagents — Task is not available at depth > 1.

Two options when full parallel coverage is required:

### Option A: Command-Orchestrated Lenses (Recommended)

The calling context spawns each lens directly as a sibling
subagent, then synthesizes results. The primary agent is
not spawned at all — only its lenses are spawned, plus a
synthesis step.

See Skill: `implementation-review-orchestration` for the
code-reviewer lens pattern.

### Option B: Sequential Fallback

Spawn the primary agent normally. The agent executes all
lens steps sequentially in a single context pass.

Agents that support sequential fallback document it in
their Research Lenses section.

## Command Integration Pattern

Commands add a short block before spawning lens-capable
agents:

```markdown
## Before Spawning {Agent}

If the target agent defines Research Lenses, follow
Skill: `parallel-research` to determine execution mode.
```
