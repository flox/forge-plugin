---
name: slice-lifecycle
description: >-
  This skill should be used when the user asks "what is
  a slice", "slice phases", "how do slices work",
  "slice workflow", or needs to understand the slice
  delivery lifecycle. Covers four phases: requirements,
  design, implementation, and completion with phase
  gates and review.
---

# Slice Lifecycle

Overview of Forge slice lifecycle. Slices are the **delivery
phase** — designing, implementing, and shipping focused
deliverables.

## What is a Slice?

**Slice:** Focused deliverable with clear scope and timeline.
**Input:** Requirements from effort (or standalone).
**Output:** Working software shipped to users.
**Duration:** Days to weeks (time-boxed).
**Location:** `.forge-context/slices/YYYYMM-{slug}/`

**Example slices:**
- Add OAuth login support
- Migrate database to new schema
- Implement export feature

## Slice Phases

### Phase 1: Requirements

**Command:** `/forge-requirements`

**Actions:**
- Define what you're building
- Define success criteria
- Identify affected components (area owners)
- Resolve open questions

**Output:**
- `requirements.md` with:
  - Summary
  - Success criteria
  - Scope (in/out)
  - Affected components
  - Open questions

**Review:** Create PR for area owner review and approval

### Phase 2: Design

**Command:** `/forge-design`

**Actions:**
- Design architecture
- Make technical decisions (ADRs)
- Break down into tasks
- Plan testing strategy

**Output:**
- `design.md` with:
  - Architecture overview
  - Integration points
  - Task breakdown (T1, T2, T3...)
  - Testing strategy
  - Key decisions (ADRs)
- `tasks.md` structure prepared

**Review:** Create PR for area owner review and approval

### Phase 3: Implementation

**Command:** `/forge-start-task`

**Actions:**
- Create tickets from task breakdown
- Implement each task in isolated worktree
- Write tests
- Create PRs

**Output:**
- Implementation PRs
- `tasks.md` updated with status

**Review:** Per-task code review

### Phase 4: Completion

**Command:** `/forge-phase-complete`

**Actions:**
- Verify all tasks complete
- Run integration tests
- Update slice status

**Output:**
- Phase completion PR
- Slice marked complete

**Review:** Final completion PR

## Slice File Structure

```
.forge-context/slices/YYYYMM-{slug}/
  requirements.md         # What we're building
  design.md               # How we're building it
  tasks.md                # Task breakdown + status
  decisions.md            # ADRs
  checklist.md            # Phase tracking
  artifacts/              # Supporting materials
    retrospective-notes.md
```

## Slice Status Tracking

Slice status is tracked in `tasks.md` (per-task status) and
`checklist.md` (phase completion tracking with dates).

**tasks.md Snapshot:**
```markdown
| Task | Description | Status | PR |
|------|-------------|--------|-----|
| T1 | Add auth model | ✅ | #42 |
| T2 | Add auth API | 🔄 | - |
```

## Phase Transitions

**Requirements → Design:**
- Requirements approved by area owners
- All open questions resolved
- Scope frozen

**Design → Implementation:**
- Design approved by area owners
- Task breakdown complete

**Implementation → Complete:**
- All tasks done
- Tests passing

**Phase gates:** Each phase requires PR approval before next
phase begins.

## When to Create a Slice

**Create slice when:**
- Clear deliverable identified
- Requirements are understood
- Scope is bounded
- Can ship in 1-3 weeks

**Defer to effort when:**
- Problem space unclear
- Discovery work needed
- Multiple deliverables
- Requirements gathering required

## Slice Workflows

### Standalone Slice (No Effort)

```
1. /forge-work new
2. /forge-requirements (gather standalone)
3. /forge-design
4. /forge-start-task (per task)
5. /forge-phase-complete
```

### Slice from Effort

```
1. /forge-work new (from effort candidate)
2. /forge-requirements (refine from effort)
3. /forge-design
4. /forge-start-task (per task)
5. /forge-phase-complete
```

## Integration with Forge Workflows

### Slice Commands

- `/forge-work new` — Initialize slice
- `/forge-requirements` — Requirements phase
- `/forge-design` — Design phase
- `/forge-start-task` — Implement task
- `/forge-phase-complete` — Complete phase
- `/forge-process-pr-discussions` — Process PR feedback

### Agents

- `requirements-gatherer` — Requirements phase
- `designer` — Design phase
- `implementation-worker` — Implement tasks
- `code-reviewer` — Review PRs
- `phase-completer` — Phase completion

## Summary

| Phase | Command | Output | Review |
|-------|---------|--------|--------|
| **Requirements** | `/forge-requirements` | requirements.md | Approval |
| **Design** | `/forge-design` | design.md, tasks.md | Approval |
| **Implementation** | `/forge-start-task` | Code PRs | Per-task |
| **Complete** | `/forge-phase-complete` | Phase PR | Approval |

**Key principles:**
- Phase gates (approval before next phase)
- Area owner review (domain expertise validation)
- Isolated work (worktrees per task)
- Evidence-based completion (tests + verification)
