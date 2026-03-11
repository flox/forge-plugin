---
name: task-breakdown
description: >-
  This skill should be used when "breaking down tasks",
  "creating task table", "parallel tracks", "shippable
  increments", or planning implementation work in a
  design. Covers deployment coupling, parallel track
  identification, task consolidation, and the task table
  format. Do not use for ticket creation (see
  /start-task).
---

# Task Breakdown Pattern

Standard approach for breaking work into independently
reviewable, shippable, and parallelizable tasks.

## Deployment Coupling Analysis

For each affected component, determine:

| Factor | Question |
|--------|----------|
| **Release cadence** | How often does this ship? |
| **Integration points** | What boundaries are crossed? |
| **Shared state** | API contracts, shared types? |

**Shipping order based on coupling:**
- Data layer changes first
- Backend/service APIs before consumer consumption
- Feature flags for incomplete user-facing work

## Parallel Track Identification

Analyze work to find parallelizable streams:

| Dependency Type | Parallelization |
|-----------------|-----------------|
| Different components, no shared contracts | Fully parallel |
| Same component, independent modules | Parallel with coordination |
| Shared API contract | Producer first, then consumer |
| Shared data | Sequential (ordering matters) |

**Output format:**
```
- Track A: Backend service implementation
- Track B: CLI/UI consumer (behind flag)
- Track C: Test infrastructure
- Sync point: Integration tests validate all tracks
```

## Shippable Increments

Each task should be:

| Criterion | Meaning |
|-----------|---------|
| **Independently mergeable** | Doesn't break main |
| **Small PRs** | Target 200-400 lines for easier review |
| **Complete** | Has tests, passes CI |
| **Flagged if needed** | Incomplete user-facing work behind flag |
| **Testable** | Can be meaningfully verified on its own |

Prefer S/M tasks; break L tasks into smaller pieces.

### Task Consolidation

**Consolidate S-sized tasks within the same component.**

Multiple trivial tasks (S-sized, ~20 lines each) to the
same component should be grouped into a single ticket/PR.
The overhead of reviewing and managing multiple tiny PRs
exceeds the benefit of granular separation.

| Scenario | Approach |
|----------|----------|
| 3 S-sized tasks, same component | Consolidate into 1 ticket |
| 2 S-sized + 1 M-sized, same component | Consider consolidating |
| S-sized tasks, different components | Keep separate |
| M or L-sized tasks | Keep separate for focused review |

**Example anti-pattern:**
```
T1: Update landing page banner (S)
T2: Remove sign-up button (S)
T3: Update install instructions (S)
```

Three separate tickets for trivially small changes to the
same component creates unnecessary overhead.

**Better approach:**
```
T1: Update pages for open access (M)
    - Update landing page banner
    - Remove sign-up button
    - Update install instructions
```

One focused ticket covering all related changes.

**When to keep tasks separate despite small size:**
- Different logical concerns
- Different reviewers needed
- Need to ship one before another for sequencing

### Testability Principle

**Don't break tasks into pieces that can't be independently
tested.**

The test for "should I split this?" is: can each piece be
meaningfully verified on its own?

If splitting creates work that can only be tested by
completing the next task, keep them together.

**Example anti-pattern (UI):**
- T1: Create dialog component
- T2: Add button that opens dialog (depends on T1)

Problem: A dialog component that isn't shown anywhere is
untestable. The real test is visual verification in the
browser — you can't see it unless it's integrated.

**Better approach:**
- T1: Create dialog + button integration (testable end-to-end)

**Exceptions to keeping tasks together:**
- Refactors and preparatory work that enable future tasks
- Infrastructure changes with their own test criteria
- Backend changes where unit tests provide sufficient coverage

## Task Table Format

```markdown
| Task | Type | Component | Size | Track | Depends On | Ticket |
|------|------|-----------|------|-------|------------|--------|
| ... | Prep/Feature | ... | S/M/L | A/B/C | ... | TBD |
```

### Type Values

| Type | Purpose |
|------|---------|
| **Prep** | Preparatory work (refactor, cleanup) — do first |
| **Feature** | Core feature implementation |

### Size Values

| Size | Approximate |
|------|-------------|
| **S** | ~20-50 lines |
| **M** | ~100-300 lines |
| **L** | ~400+ lines (consider splitting) |

## Complexity Thresholds

Watch for these warning signs:

| Threshold | Warning |
|-----------|---------|
| > 10 tasks | Consider splitting into multiple slices |
| > 3 L-sized tasks | High complexity warning |
| > 4 affected components | Cross-cutting complexity |

If thresholds exceeded, consider whether scope should be
reduced.

## Ordering

1. Prep tasks first (create clean foundation)
2. Feature tasks by dependency order
3. Group prep tasks at top for visibility
