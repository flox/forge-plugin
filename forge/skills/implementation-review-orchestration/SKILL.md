---
name: implementation-review-orchestration
type: orchestration
description: >-
  This skill should be used when a command needs the
  full implement-and-review cycle — spawning an
  implementation worker, running a code review gate, and
  making a post-review decision. Used by /forge-start-task
  and /forge-implement. Do not use for review-only or
  implementation-only workflows.
---

# Implementation Review Orchestration

Thin dispatcher pattern for the implement-then-review pipeline.
The main context manages control flow and reads structured
signals from sub-agents. All analysis and synthesis happens
inside sub-agents, not here.

## When to Use

Commands load this skill when they need to:
1. Spawn an implementation worker for code changes
2. Run a code review gate on the resulting PR
3. Make a post-review decision (ready vs re-work)

**Commands that use this skill:**
- `/forge-start-task`
- `/forge-implement`

## Three-Step Pipeline

### Step 1: Spawn Worker

Spawn the implementation worker and read its completion
signal. The worker creates a draft PR and returns a
structured report.

```
Use Task tool with:
- subagent_type: "Implementation Worker"
- mode: "bypassPermissions"
- prompt: |
    ## Inputs
    {ticket/change context from calling command}
```

**Read signal from worker:**
```
{ pr_url, commit_sha, status: completed|blocked }
```

- If `status: blocked`: report blocker to user, stop.
- If `status: completed`: proceed to Step 2.

### Step 2: Code Review Gate

Three paths based on change characteristics. The calling
command selects the path; this skill documents each.

#### Path A: Simple Review (default)

For changes <=50 lines, low risk, well-established
patterns. Spawn a single code-reviewer in sequential mode.

```
Use Task tool with:
- subagent_type: "Code Reviewer"
- mode: "bypassPermissions"
- prompt: |
    ## Inputs
    - pr_url: {from Step 1 signal}
    - project: {project}
    - feature_path: {feature_path}

    Execute the review and post results to the PR.
```

**`bypassPermissions` is required.** The reviewer uses
shell commands to post the review to GitHub and to retrieve
the project SHA for the signature. Without
`bypassPermissions`, shell calls will be auto-denied in
non-interactive sessions.

**Read signal from reviewer:**
```
{ findings: [...], severity_max, passed }
```

#### Path B: Full Parallel Review

For changes >50 lines, security-sensitive areas, or new
architectural patterns. Spawn 3 lens sub-agents in a
single message, then synthesize.

**Spawn 3 lenses in one message (parallel):**

```
# Lens A: Security & Correctness
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: |
    Review PR {pr_url} through security and correctness
    lens. Check for: injection vectors, auth bypasses,
    data validation gaps, logic errors, race conditions.
    Return structured findings with severity labels.

# Lens B: Performance & Architecture
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: |
    Review PR {pr_url} through performance and
    architecture lens. Check for: N+1 queries,
    unbounded allocations, layering violations.
    Return structured findings with severity labels.

# Lens C: Conventions & Tests
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: |
    Review PR {pr_url} through conventions and testing
    lens. Check for: style violations, missing tests,
    test quality, naming conventions, doc gaps.
    Return structured findings with severity labels.
```

**After all 3 complete, spawn synthesis sub-agent:**

```
Use Task tool with:
- subagent_type: "general-purpose"
- mode: "bypassPermissions"
- prompt: |
    Synthesize these three code review perspectives
    into a single review post for PR {pr_url}.

    ## Lens A: Security & Correctness
    {paste Lens A output}

    ## Lens B: Performance & Architecture
    {paste Lens B output}

    ## Lens C: Conventions & Tests
    {paste Lens C output}

    Deduplicate findings, assign final severity,
    and post the synthesized review to the PR.
    Include project signature.
```

**Read signal from synthesis:**
```
{ findings: [...], severity_max, passed }
```

#### Path C: Agent Teams (experimental)

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled
and the user opts in. Create a team with 3 lens
teammates that can cross-pollinate findings in real-time.

Prompt user before using teams:
```
question: "Use agent team for richer code review?
  Teammates can challenge each other's findings."
options:
  - "Use a team (Recommended)"
  - "Standard parallel mode"
```

If user selects teams, create a team with one teammate
per lens. Otherwise fall back to Path B.

### Step 3: Post-Review Decision

Read the review signal and decide:

**Critical or Important findings exist:**
- Report findings summary to user
- Offer options:
  1. Re-spawn worker to address findings
  2. Handle manually
  3. Proceed anyway (user override)

**Minor or no findings:**
- Mark PR ready: `gh pr ready {pr_number}`
- Post readiness summary with project signature

## Thin Dispatcher Contract

The main context (command) acts as a thin dispatcher:

- **DO** read structured signals from sub-agents
- **DO** make routing decisions (which path, re-work?)
- **DO** present summaries and options to the user
- **DO NOT** analyze code or review findings yourself
- **DO NOT** synthesize review results in main context
- **DO NOT** reference other orchestration skills

All analytical work happens inside sub-agents. The main
context budget for this pipeline is ~100 lines of
signal handling.

## Nesting Rule

This skill is self-contained. It does not reference
or depend on any other orchestration skill. Commands
may load this skill sequentially after other
orchestration skills complete, but that is command-level
sequencing, not orchestration nesting.
