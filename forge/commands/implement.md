# /implement

Ad-hoc code changes without slice ceremony.

## This Command's Role

Lightweight entry point for small, well-understood changes
that don't warrant full slice lifecycle. Captures a
description, spawns the designer for context-aware analysis,
presents a change plan for approval, optionally creates a
GitHub issue, then delegates to the implementation worker.

**Key principle: Analyze before changing.** The designer
identifies all touch points and risks before any code is
modified.

## Bash Command Guidelines

When using bash commands:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Use `test -f` or `[ -f ]` before file operations
- Avoid commands that error on normal condition checks
- Use exit codes for control flow, not error messages

## Workflow

### Step 1: Capture Description

If the user provided a description with the command, use
it. Otherwise ask:

> "What change do you want to make? Describe it in plain
> language — what should change and why."

Accept free-form input. No structured triage needed.

### Step 2: Spawn Designer (Adhoc Mode)

The designer agent defines Research Lenses. Before
spawning, follow Skill: `parallel-research` to determine
execution mode (parallel vs sequential lens evaluation).

Spawn the designer agent to analyze the change and
identify all touch points across the codebase.

```
Use Task tool with:
- subagent_type: "Designer"
- prompt: |
    ## Inputs
    - mode: "adhoc"
    - change_description: {user's description}

    Analyze the change and return a structured change plan.
    Do NOT write any files — return the plan as your
    response.
```

The designer reads context files, explores the codebase,
and returns a structured change plan with affected files,
change order, and risks.

### Step 3: Present Change Plan (HARD GATE)

Display the designer's change plan to the user. This is
a mandatory approval gate — no code changes happen without
explicit user approval.

> **Change Plan**
>
> {designer's structured output}
>
> Proceed with implementation?

Options:
- "Proceed (Recommended)"
- "Modify" — user wants to adjust the plan
- "Cancel"

If "Modify": ask what to change, re-run designer with
updated description. If "Cancel": stop.

### Step 4: GitHub Issue (Optional)

After plan approval, offer to create a tracking issue
in the primary target repo:

> "Create a GitHub issue for this change?"

Options:
- "Create issue (Recommended)"
- "Skip — no issue needed"

If creating an issue:
1. Derive title from the change plan
2. Build body with rationale, affected files, and
   acceptance criteria
3. See Skill: `forge-signature` for signature pattern
4. Show issue details for user confirmation before creating
5. Create with `gh issue create`
6. Capture the issue number for the implementation step

### Step 5: Implement

Spawn the implementation worker with the approved plan.
The named `subagent_type` auto-loads the full agent
definition — the prompt provides inputs only.

```
Use Task tool with:
- subagent_type: "Implementation Worker"
- mode: "bypassPermissions"
- prompt: |
    ## Inputs
    - ticket_number: {issue number if created, or "none"}
    - repository: {target repo, e.g., org/repo}
    - worktree_path: (create per worktree conventions)
    - feature_path: (none — ad-hoc change)
    - project: {primary affected project}

    ## Change Plan (Approved)
    {designer's structured output — paste the full
     change plan as the agent's specification}

    ## Target Repository
    {primary repo path}
```

**`bypassPermissions` is required** so the worker can
use Write and Bash in target repositories without
permission denials. The worker operates in an isolated
worktree — all changes go through PR review.

The worker creates a draft PR and returns a completion
report. It does **not** spawn the code-reviewer.

### Step 5.5: Code Review Orchestration

After the worker completes, run the review gate from
Skill: `implementation-review-orchestration` (Step 2
only — the worker already ran in Step 5).

Select the review path based on change size:
- **Path A** (simple): <=50 lines, low risk
- **Path B** (full parallel): >50 lines, security
- **Path C** (teams): experimental, if enabled

After review completes, follow Step 3 (post-review
decision) from the same skill.

### Step 6: Summary

After implementation and code review:

> **Implementation Complete**
>
> - Files changed: {list}
> - Tests run: {pass/fail summary}
> - Code review: {pass/findings summary}
> - Issue: {link if created}
> - PR: {link}
>
> {any notes or warnings from the worker}

## Example Interaction

```
User: /implement add a new catalog endpoint
      for anonymous users

Agent: [spawns designer in adhoc mode]

Agent: **Change Plan**
       Affected: api/ (Primary)
       Files to Modify:
       - src/api/routes.py:34 — Add endpoint
       - src/api/auth.py:45 — Bypass auth for anon
       Proceed with implementation?

User: Proceed

Agent: Create a GitHub issue for this change?

User: Skip

Agent: [spawns implementation worker]

Agent: **Implementation Complete**
       Files changed: 2
       Tests: 12 passed, 0 failed
       Branch: feat/add-anon-catalog-endpoint
```

## Subcommands

None — this command enters interactive mode directly.

## Writing Guidelines

Follow `.forge-context/context/principles.md` conventions:
- Active voice, no filler words
- Concise and direct
