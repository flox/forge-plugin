# Implementation & Review Workflow

Implementation in Forge follows a strict delegation model:
the orchestrating command never writes code itself. Instead,
it spawns an Implementation Worker agent that follows TDD
discipline, then gates the result through a code review
before marking the PR ready.

---

## Context Isolation Per Ticket

Each implementation task receives a self-contained brief
that gives the worker everything it needs without loading
the full design. This is the context cascade from the
[design workflow](design-workflow.md) paying off.

```mermaid
flowchart LR
    D["design.md"] --> DA["design-agentic.md"]
    DA --> TB["ticket-brief-t1.md"]
    TB --> W["Implementation Worker<br/>(isolated worktree)"]

    style TB fill:#f4e8e8
```

The worker's context loading follows a priority cascade:

1. **Ticket brief** (standalone spec — stop here if found)
2. **`design-agentic.md` + `design.md`** (both required)
3. **`design.md` alone** (with a warning)

This means a worker for ticket T3 never sees T1's or T2's
implementation details — only its own brief and the
project's existing codebase patterns.

---

## Implementation Worker Phases

The worker executes 8 phases, from context gathering
through PR creation. Several quality disciplines are
embedded directly in the phase sequence.

```mermaid
flowchart TB
    P0["Phase 0: Work Mode<br/>(new ticket vs PR follow-up)"]
    P05["Phase 0.5: Worktree Setup"]
    P1["Phase 1a: Gather Context<br/>• Read ticket + design artifacts<br/>• Discover code patterns<br/>• Context verification checkpoint"]
    P15["Phase 1.5: Extract Design Specs<br/>(working-memory checklist)"]
    P2["Phase 2: Explore Existing Code<br/>(grep before you code)"]
    P3["Phase 3: Plan Implementation"]

    P4["Phase 4: Implement<br/>(TDD: RED-GREEN-REFACTOR)"]
    P45["Phase 4.5: Design Compliance<br/>Checkpoint"]
    P5["Phase 5: Verify<br/>(evidence-based completion)"]
    P6["Phase 6: Create Draft PR"]
    P7["Phase 7: Report for Review"]

    P0 --> P05 --> P1 --> P15 --> P2 --> P3
    P3 --> P4 --> P45 --> P5 --> P6 --> P7

    style P4 fill:#f4e8e8
    style P45 fill:#e8e8f4
    style P5 fill:#e8f4e8
```

### TDD Discipline (Phase 4)

The RED-GREEN-REFACTOR cycle is enforced during
implementation:

```mermaid
flowchart LR
    R["RED<br/>Write failing test"] --> G["GREEN<br/>Minimal code to pass"]
    G --> RF["REFACTOR<br/>Improve quality"]
    RF --> R

    R -. "must FAIL<br/>for the right reason" .-> R
    G -. "must PASS<br/>no extras yet" .-> G
    RF -. "tests still pass<br/>no behavior change" .-> RF
```

**Strong TDD candidates:** Business logic, error handling,
data transformations, API endpoints, database queries.

**Pragmatic exceptions:** Nix expressions (test with
`nix build`), generated code (test the generator),
configuration files (validate with schema), simple
refactors (existing tests provide coverage).

Evidence is captured in commit messages — either
"TDD: RED-GREEN-REFACTOR" or the exception reason.

### Design Compliance Checkpoint (Phase 4.5)

After implementation but before testing, the worker
verifies each spec category against the design:

- Data structures match
- Authorization uses the correct project pattern
- Feature flags all implemented
- Edge cases handled as designed
- API contracts match
- Constants use exact design values

Any accidental deviation is fixed immediately. Intentional
deviations require explicit user approval.

### Verification Before Complete (Phase 5)

"Done" means "verified", not "attempted." The worker must
produce concrete evidence:

| Change Type | Verification |
|------------|--------------|
| Code changes | Test output showing pass |
| Build changes | Build logs showing success |
| Bug fixes | Before (error) and after (clean) |
| Refactors | Full test suite, same count |

Unacceptable evidence: "I think it works", "should be
fine", "tests probably pass."

---

## Code Review Orchestration

After the worker produces a draft PR, the orchestration
skill selects one of three review paths based on the
change characteristics.

```mermaid
flowchart TB
    W["Implementation Worker<br/>completes with draft PR"]
    W --> D{"Change<br/>characteristics?"}

    D -- "≤50 lines<br/>low risk" --> A["Path A: Simple Review<br/>(single Code Reviewer)"]
    D -- ">50 lines or<br/>security-sensitive" --> B["Path B: Parallel Review<br/>(3 lens agents + synthesis)"]
    D -- "Teams available<br/>+ user opt-in" --> C["Path C: Agent Teams<br/>(experimental)"]

    A --> POST["Post-Review Decision"]
    B --> POST
    C --> POST

    style A fill:#e8f4e8
    style B fill:#e8e8f4
    style C fill:#f4f4e8
```

### Path A: Simple Review

A single Code Reviewer agent (Opus) runs the full
two-stage review process.

### Path B: Full Parallel Review

Three lens agents run in parallel, each focusing on a
different dimension:

```mermaid
flowchart TB
    PR["Draft PR"] --> L1["Security &<br/>Correctness<br/>(Opus)"]
    PR --> L2["Performance &<br/>Architecture<br/>(Opus)"]
    PR --> L3["Conventions &<br/>Tests<br/>(Opus)"]

    L1 --> SYN["Synthesis Agent<br/>(Opus)"]
    L2 --> SYN
    L3 --> SYN

    SYN --> REV["Unified Review<br/>(posted to PR)"]
```

The synthesis step deduplicates findings across lenses,
assigns final severity, and structures the result into
the two-stage review format.

### Two-Stage Review Structure

The Code Reviewer uses a gated review process — Stage 2
only runs if Stage 1 passes.

**Stage 1: Spec Compliance** (gates Stage 2)
- Requirements alignment
- Design alignment
- Test coverage alignment
- Intent coverage (if `intent-spec.md` exists)

**Stage 2: Code Quality** (only if Stage 1 passes)
- Security (Critical)
- Correctness (Critical/Important)
- Error handling (Important)
- Performance (Important)
- Maintainability (Important/Minor)
- Style (Minor)

Severity classification:

| Level | Meaning | Action |
|-------|---------|--------|
| **C** (Critical) | Security, data loss, production-breaking | Block merge |
| **I** (Important) | Maintainability, performance, patterns | Fix or ticket |
| **M** (Minor) | Cosmetic, stylistic | Optional |

---

## Full Pipeline

The complete implement-and-review cycle, showing how
the orchestration skill acts as a thin dispatcher.

```mermaid
sequenceDiagram
    participant CMD as Command<br/>(forge-start-ticket)
    participant W as Implementation<br/>Worker (Sonnet)
    participant CR as Code Reviewer<br/>(Opus)
    participant GH as GitHub PR
    participant U as User

    CMD->>W: Spawn with ticket context
    W->>W: TDD: RED-GREEN-REFACTOR
    W->>W: Design compliance check
    W->>W: Verification (tests + evidence)
    W->>GH: Create draft PR
    W->>CMD: Signal: { pr_url, status }

    alt status: blocked
        CMD->>U: Report blocker, STOP
    else status: completed
        CMD->>CR: Spawn review
        CR->>CR: Stage 1: Spec compliance
        alt Stage 1 FAIL
            CR->>CMD: Findings (stop at Stage 1)
        else Stage 1 PASS
            CR->>CR: Stage 2: Code quality
            CR->>GH: Post review with findings
            CR->>CMD: Signal: { findings, passed }
        end
    end

    alt Critical/Important findings
        CMD->>U: Report findings
        U->>CMD: Re-spawn worker / Handle manually / Override
    else Minor or no findings
        CMD->>GH: gh pr ready
        CMD->>GH: Post readiness summary
    end
```

### Post-Review Decision Loop

When the review surfaces Critical or Important findings,
the user has three options:

1. **Re-spawn worker** — The worker receives the findings
   and addresses them, then re-enters the review cycle
2. **Handle manually** — The user fixes issues themselves
3. **Override** — Proceed despite findings (rare, for
   time-sensitive situations)

Minor findings or a clean review result in the PR being
marked ready for merge automatically.

---

## Architectural Constraints

Several design decisions enforce the delegation model:

- **Implementation Worker cannot spawn subagents** —
  The Task tool is unavailable to it, preventing it from
  creating its own review pipeline
- **Code Reviewer cannot spawn subagents** — Lens agents
  are spawned by the calling context, not the reviewer
- **Orchestration is a thin dispatcher** — The command
  reads structured signals and makes routing decisions;
  it never analyzes code or synthesizes results itself
- **`bypassPermissions`** is set on both Worker and
  Reviewer spawns for Bash access in non-interactive
  sessions
