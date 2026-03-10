---
name: pr-discussion-orchestration
type: orchestration
description: >-
  This skill should be used when
  /forge-process-pr-discussions needs to orchestrate its
  three-phase pipeline — analyze unresolved threads,
  delegate changes to specialized agents, then resolve
  threads. Do not use outside the PR discussion
  processing command.
---

# PR Discussion Orchestration

Thin dispatcher pattern for processing PR discussion threads.
The main context manages the three-phase pipeline; all
analysis and change application happens inside sub-agents.

## When to Use

The `/forge-process-pr-discussions` command loads this skill
to orchestrate the PR discussion processor and any delegate
agents it spawns.

## Three-Phase Pipeline

### Phase 1: Analyze

Spawn the `pr-discussion-processor` to fetch the PR,
identify unresolved threads, group by theme, and produce
a delegation plan.

```
Use Task tool with:
- subagent_type: "PR Discussion Processor"
- prompt: |
    ## Inputs
    - pr_number: {number}
    - owner: {owner}
    - repo: {repo}
    - feature_path: {path}
```

**Read signal:**
```
{ delegation_plan, thread_count, pr_type }
```

### Phase 2: Delegate Changes

Based on the delegation plan, spawn the appropriate agent
to apply changes:

| PR Type | Delegate Agent |
|---------|---------------|
| Implementation | implementation-worker |
| Design | designer |
| Requirements | requirements-gatherer |
| Other markdown | pr-discussion-processor (direct) |

**Separation of concerns:** When Phase 2 delegates to the
implementation-worker, the worker applies changes and reports.
It does **not** chain into code review. Review is a separate
concern handled by the calling command after all three phases
complete. If review is needed, the command loads the review
orchestration skill step 2 only (the worker already ran).

**Read signal from delegate:**
```
{ commit_sha, changes_applied, status }
```

### Phase 3: Resolve

Spawn the pr-discussion-processor again (or continue if in
same context) to reply to threads and resolve them based
on the changes applied.

**Read signal:**
```
{ resolved: N, remaining: M, actions: [...] }
```

## Thin Dispatcher Contract

The main context manages phase transitions and reads signals.
It does not analyze PR content, classify threads, or apply
changes directly.

- Phase 1 output feeds Phase 2 input
- Phase 2 output feeds Phase 3 input
- Main context budget: ~35 lines of signals

## Nesting Rule

This skill is self-contained. It does not reference
or depend on any other orchestration skill. The calling
command may load the review orchestration skill after this
pipeline completes for a review gate, but that is sequential
command-level composition, not nesting.
