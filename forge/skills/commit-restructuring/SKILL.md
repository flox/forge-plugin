---
name: commit-restructuring
description: >-
  This skill should be used when "restructuring commits",
  "organizing PR history", "making commits reviewable",
  or planning how to split work into atomic commits. The
  intellectual foundation for /reviewable. Do not
  use for writing commit messages (see git workflow
  guideline).
---

# Commit Restructuring

How to transform development history into commits that reviewers
can evaluate efficiently. These principles guide both manual
commit organization and the `/forge:reviewable` automated
workflow.

## When to Reference

- Before restructuring commits for a PR
- When planning how to organize work into commits
- When reviewing whether a commit sequence tells a clear story
- When the `/forge:reviewable` command needs guidance

## Core Principle: Organize by Review Concern

Group changes by what type of **review thinking** they require,
not by file proximity. Changes in the same file that need
different review thinking belong in different commits.

Ask: "What does a reviewer need to think about to evaluate
this correctly?"

### Review Concern Categories

| Concern | Type | Reviewer Thinking |
|---------|------|-------------------|
| Configuration | `chore` | Structured correctly? Sensible defaults? |
| Data layer | `feat`/`refactor` | Schema right? State safe? |
| Observability | `chore` | Right signals? Passive, no behavior change |
| Auth/Authz | `feat` | Secure? Access controlled? Always isolate |
| Testing | `test` | Right cases? Edge cases covered? |
| Build/Packaging | `chore` | Artifact correct? Dependencies right? |

Auth/Authz changes warrant isolation because security review
requires focused attention that degrades when mixed with other
concerns.

### Example: Same File, Different Concerns

```
Wrong (organized by file):
Commit: "Update auth.py"
  + from jwt import decode       # Auth concern
  + import prometheus_client     # Observability concern
  + def verify_jwt(token): ...  # Auth concern
  + metrics.inc('auth_attempts') # Observability concern

Right (organized by review concern):
Commit 1 (feat): "Add JWT verification"
  + from jwt import decode
  + def verify_jwt(token): ...

Commit 2 (chore): "Add auth attempt metrics"
  + import prometheus_client
  + metrics.inc('auth_attempts')
```

## The Storytelling Principle: Paint, Don't Move

Each commit should add detail to an evolving story, like a
painter building up a canvas — not like a mover shuffling boxes
between rooms.

### The Painting Progression

1. **Sketch** — Types, interfaces, signatures (even stubbed)
2. **Block in** — Core implementations with context
3. **Detail** — Refinements, edge cases, integration
4. **Polish** — Cleanup, documentation, final touches

### Bad Story (Moving)

```
Commit 1: Move User model to new file
Commit 2: Move Auth logic to new file
Commit 3: Move tests to new file
```

Reviewer sees file movements with no understanding of why.

### Good Story (Painting)

```
Commit 1: Add authentication abstraction
  (trait + types, TODO for implementations)
Commit 2: Implement primary auth strategy
  (fills in from abstract established in commit 1)
Commit 3: Wire auth into application
  (shows how commit 2 integrates into the system)
Commit 4: Add tests validating auth flow
  (proves commits 1-3 work together)
```

Each commit makes sense given what came before.

### Story Structure Rules

- **Introduce before using** — show the interface before the
  implementation
- **Use TODOs to signal future commits** — `TODO(NEXT_COMMIT)`
  tells reviewers "this is coming"
- **Build context incrementally** — each commit understandable
  based only on previous commits
- **Respect review concern boundaries** — even while building
  the story, keep concerns separated

## Commit Type as Hard Constraint

The commit type signals review importance from the author.
Treat it as a hard constraint when restructuring.

- `feat:` — new feature, affects behavior
- `fix:` — bug fix, affects behavior
- `chore:` — maintenance, no behavior change
- `refactor:` — structure change, behavior unchanged
- `test:` — test changes only

When restructuring, preserve the original author's type intent.

## The "And" Rule

If a commit description needs the word "and", split the commit.
"And" indicates multiple concerns mixed together.

- Wrong: "Add auth validation and refactor error handling"
- Right: Two commits — "Add auth validation" then "Refactor
  error handling"

## Pure Moves

Moving code between files without logic changes is a single
atomic unit. Git detects the move automatically.

Preferred: one commit with deletion from old location and
addition to new location.

### Move + Enhance

When code is both relocated AND modified, split into two:

1. **Pure relocation commit** — copy to new location, delete
   from old. No behavioral changes. Git detects the move.
2. **Enhance commit** — add new behavior, extend interfaces,
   modify logic. Reviewable as clean diff against relocated code.

**This separation is mandatory** — a reviewer must be able to
distinguish "this code moved here" from "this code is new".

## Build Safety

Every commit must leave the codebase compilable, testable, and
runnable. This enables `git bisect` and lets reviewers check
out any commit to test.

### Signature Changes

When changing method signatures or public APIs:

```
Commit 1: Extract to strategy (backwards compatible)
  - New parameter optional with default
  - Mark with TODO(MIGRATION)
Commit 2: Add new implementations
Commit 3: Update all callers (remove defaults)
Commit 4: Remove deprecated parameters
```

## Zero Loss Guarantee

After restructuring, the final state must match the original
state exactly. Verification uses dual-branch comparison:

1. Record the original branch tip commit hash before starting
2. Create restructured commits on a new ephemeral branch
3. Compare: `git diff <original-tip> <restructured-tip>`
   — must be empty

The original branch is never modified.

## Review Depth

Each commit carries a review depth signal — how much scrutiny
a reviewer should give it.

### Depth Levels

| Depth | Signal | Reviewer Action |
|-------|--------|-----------------|
| **high** | Behavior, architecture, or security change | Deep focus — trace logic, check edge cases |
| **medium** | Substantive but lower risk | Normal review — check correctness |
| **low** | Mechanical or cosmetic | Quick scan — verify it looks right |

### Criteria for Each Level

**high** — could break things or introduce vulnerabilities:
- New or changed behavior (features, bug fixes)
- Architecture changes (new patterns, restructured pipelines)
- Security-sensitive changes (auth, crypto, input validation)
- Data model changes (schema, migrations)
- API contract changes

**medium** — substantive work with lower risk:
- Tests
- Configuration with behavioral impact
- Error handling changes
- Significant refactors

**low** — mechanical changes:
- Pure code moves (100% git similarity)
- Formatting, whitespace, style
- Trivial renames
- Documentation updates

## Commit Message Format

Follow conventional commits with review depth trailers:
```
<type>(<scope>): <subject>

<body explaining why, not what>

Review-depth: <high|medium|low>
Review-reason: <one-line why this depth>
```

Types: `feat`, `fix`, `refactor`, `test`, `style`, `chore`,
`docs`

The body should explain WHY the change exists.

The `Review-depth` and `Review-reason` trailers help reviewers
triage their attention across many commits.

## Line-Level Staging

Different logical changes in the same file belong in different
commits — whole-file staging only applies when the entire file
is a single unit of change.

For surgical staging of specific hunks within files:

```bash
# Extract specific hunks as a patch
git diff HEAD -- <file> > /tmp/full.patch
# Edit patch to keep only desired hunks
# Apply to staging area without modifying working tree
git apply --cached /tmp/selected.patch
```
