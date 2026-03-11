# /design

Run the design phase for a slice with approved requirements.

The command detects which design artifacts exist and guides
the user through a progressive path:

1. **Approach** (`design-approach.md`) — strategic direction
   via parallel research lenses
2. **Full design** (`design.md`) — implementation-ready spec
3. **Enrich** (`design-agentic.md` + task briefs) —
   optional agent handoff preparation

The command detects current state and suggests the next
step. After approach completes, it offers to continue
directly to full design.

## This Command's Role

Interactive wrapper that verifies prerequisites and
identifies the feature, then delegates to the `Designer`
agent for the full design process.

**Always use this command (and the Designer agent) for
design phase work.** The designer's phased approach
ensures structural completeness — ADRs, decision
verification, design constraints, code references, and
checklist updates.

## Terminology Awareness

Before producing any user-facing output, read
`.forge-context/overrides/terminology.md`. If the user
has mapped Forge terms to their own vocabulary, use
their terms in all output — menus, status messages,
suggestions, and agent prompts. Pass the mapped terms
to any spawned agents so they also use the user's
language.

## Behavior

### Step 1: Identify Current Slice

Check current working directory or ask:
> "Which slice are you working on?"

**CRITICAL: When in a worktree, read slice files from
the WORKTREE path:**
```
Correct: /path/to/_worktrees/{slug}/.forge-context/slices/{YYYYMM}-{slug}/checklist.md
Wrong:   /path/to/project/.forge-context/slices/{YYYYMM}-{slug}/checklist.md
```

### Step 2: Verify Prerequisites

Check `{slice_path}/checklist.md` for requirements
completion. If requirements phase not complete:

> "Requirements phase is not yet complete."
> "Please complete requirements first with
> `/requirements` or mark as complete."
> "Continue anyway? (yes/no)"

### Step 2.7: Detect Design State and Route

Check which design artifacts exist:

```bash
test -f "{slice_path}/design-approach.md"
test -f "{slice_path}/design.md"
test -f "{slice_path}/design-agentic.md"
```

**State A — No design-approach.md:**

> "No design approach found. The approach step explores
> architectural direction through parallel research
> lenses before detailed design.
>
> 1. Start with approach exploration (Recommended)
> 2. Skip to full design
> 3. Cancel"

If 1 → `mode = "approach"`. If 2 → `mode = "full"`.

**State B — Approach exists, no design.md:**

> "Design approach exists. Ready for full design.
>
> 1. Continue to full design (Recommended)
> 2. Re-run approach exploration
> 3. Cancel"

If 1 → `mode = "full"`. If 2 → `mode = "approach"`.

**State C — Both approach and design.md exist:**

> "Full design exists.
>
> 1. Enrich for agent implementation (optional —
>    adds behavioral depth and per-task briefs)
> 2. Re-run full design
> 3. Done — proceed to review"

If 1 → `mode = "enrich"`. If 2 → `mode = "full"`.
If 3 → skip to Step 5 (offer review).

### Step 2.8: Assess Team Design Mode (Full Mode Only)

When `mode == "full"`, do a lightweight scan for
multi-subsystem complexity.

**If `design-approach.md` exists:**
Read it and count distinct components with cross-boundary
interactions. If 3+ subsystems are identified, offer team
mode to the user. Include token cost caveat.

**If no design-approach.md:**
Quick-scan `requirements.md` for signals of multi-subsystem
complexity (3+ components, multiple external integrations,
complex cross-component data flows). If signals present,
note team mode is available after approach completes.

**If user selects team mode:**
Follow Skill: `team-design` for the 3-stage process
(decompose → parallel designers → synthesize). The command
acts as team lead. Skip Step 3 below.

**If user selects standard mode:**
Continue to Step 3.

### Step 3: Spawn Designer

**If mode is "approach":** The designer defines Research
Lenses. Before spawning, follow Skill: `parallel-research`
to determine execution mode.

**If mode is "full" or "enrich":** Spawn normally.

```
Use Task tool with:
- subagent_type: "Designer"
- prompt: |
    ## Inputs
    - feature_path: {feature_path}
    - feature_name: {feature_name}
    - mode: "{mode}"
```

**Mode behavior:**

| Mode | Output | Interaction |
|------|--------|-------------|
| approach | design-approach.md | Conversational |
| full | design.md + decisions.md | Comprehensive |
| enrich | design-agentic.md + task briefs | Autonomous |

### Step 3.5: Chain to Next Step

**After approach completes:**
> "Approach documented. Continue to full design now?"
> 1. Yes — continue to full design (Recommended)
> 2. No — stop here for now

If yes, loop back to Step 2.8 with `mode = "full"`.

**After full design completes:**
Continue to Step 4 (report) and Step 5 (review).

### Step 4: Report Completion

Display the subagent's summary:
- Design complete
- Key decisions made
- Task breakdown
- Suggested reviewers
- Next steps

### Step 5: Design Review Gate

After design completes, offer validation before review:

> "Design document complete! The designer recommends
> running the Design Reviewer to validate requirements
> coverage before review.
>
> Would you like to:
> 1. Run Design Reviewer now (recommended)
> 2. Skip and submit PR directly
> 3. Review design yourself first"

**If user selects option 1:**

```
Use Task tool with:
- subagent_type: "Design Reviewer"
- prompt: |
    ## Inputs
    - slice_path: {slice_path from designer output}
    - slice_name: {feature_name}

    Execute the review and save the report to
    {slice_path}/artifacts/design-review-report.md.
```

After design-reviewer completes, read the result:
- PASS or PASS with suggestions → mark PR ready
- NEEDS REVIEW or BLOCKED → report findings, offer to
  re-spawn designer to address them

**If option 2 or 3:**
Proceed with next steps. Remind user they can run
design-reviewer later via `/work review`.

## Context Files to Read

- `.forge-context/slices/` — To identify current slice
- `{slice_path}/checklist.md` — To verify prerequisites

**Note:** When working in a worktree, `{feature_path}`
refers to the worktree location, not the main branch.

## Example Interactions

### Fresh Start (no design artifacts)
```
User: /design

Agent: Working on **CUDA Build Support**.
       Requirements phase is complete.

       No design approach found.
       1. Start with approach exploration (Recommended)
       2. Skip to full design
       3. Cancel

User: 1

Agent: [spawns designer in approach mode with lenses]
       [Lenses: Architecture Options, Ecosystem Patterns,
       Risk & Constraints, Devil's Advocate]
       [Designer converses, documents choices]

Agent: Approach documented. Continue to full design now?
       1. Yes — continue (Recommended)
       2. No — stop here

User: 1

Agent: [spawns designer in full mode]

Agent: Design complete for CUDA Build Support:
       - 3 key decisions documented
       - 6 implementation tasks identified

       Run Design Reviewer before review?
       1. Yes (recommended)
       2. Skip
       3. Review yourself first
```

### Resuming (approach already done)
```
User: /design

Agent: Working on **CUDA Build Support**.
       Design approach exists. Ready for full design.

       1. Continue to full design (Recommended)
       2. Re-run approach exploration
       3. Cancel

User: 1

Agent: [spawns designer in full mode]
```
