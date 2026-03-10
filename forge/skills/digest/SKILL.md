---
name: digest
description: >-
  Generate activity digests and summaries of what happened
  in Forge. Use whenever the user asks "what happened",
  "catch me up", "what changed", "summary of activity",
  wants a digest, status update, or standup/sprint prep.
  Also use for questions about recent decisions, phase
  transitions, or active discussions. Even if the user
  doesn't say "digest" explicitly — any request to
  understand recent Forge activity should use this skill.
---

# Digest Pattern

Generate concise "what happened" summaries for Forge activity.
Digests focus on **semantic changes** — decisions, phase
transitions, new work, direction shifts — not raw commit
counts or file diffs.

## When to Use

- User asks "what happened" / "catch me up" / "summary"
- Agent needs to contextualize recent activity
- Any context where recent Forge changes matter

## Duration Resolution

Parse the user's duration into a `git --since` value:

| Input | Resolution |
|-------|------------|
| `daily` | 24 hours ago |
| `weekly` | 7 days ago |
| `monthly` | 30 days ago |
| `since YYYY-MM-DD` | Exact date |
| `last N days/weeks` | N days/weeks ago |

## Scope Definitions

### Scope: `efforts`

Signal to extract (priority order):

1. **New efforts** initialized in period
2. **Decisions** — new ADR entries in `decisions.md`
3. **Story refinement** — stories moving to ready/in-slice
4. **Slice candidates** — new candidates accepted/spawned
5. **Scope changes** — in/out boundaries shifting

Git filter: `-- .forge-context/efforts/`

### Scope: `slices`

Signal to extract (priority order):

1. **Phase transitions** — requirements → design →
   implementation → complete
2. **Decisions** — new ADR entries in `decisions.md`
3. **Architecture/direction changes** — `design.md` changes
   that alter approach, not just fill in details
4. **Completion** — slices marked done
5. **New slices** spawned in period

Git filter: `-- .forge-context/slices/`

### Scope: `forge`

Signal to extract:

1. **New/changed agents or commands** — capability shifts
2. **Guideline changes** — engineering standard updates
3. **Context updates** — domain knowledge changes
4. **New skills** added

### Scope: `all`

Combine all three scopes above. This is the default when
no scope is specified.

## Significance Filtering

Not everything that changed is worth reporting. Apply these
rules to separate signal from noise:

**Always significant:**
- Decisions (ADRs) — any new entry in `decisions.md`
- Phase transitions — checklist phase completions
- New work items — new efforts or slices initialized
- Completions — work marked done

**Significant if substantive:**
- Content changes — only when they alter direction, scope,
  or architecture (not typo fixes or formatting)
- Design updates — approach changes, not detail fill-ins

**Usually noise (skip unless meaningful):**
- `fix(audit)` — automated audit fixes
- `chore(` — routine maintenance
- Formatting-only changes
- Index/README auto-updates

## Output Format

```markdown
# Digest: {Scope} | {Duration Label}

**Period:** YYYY-MM-DD to YYYY-MM-DD

## Key Highlights

- {1-2 sentence executive summary, most important items only}

## Efforts

### New
- **Name** — problem statement (few words)

### Decisions
- **Effort Name** — ADR-N: Title

### Candidate Movement
- **Effort Name** — N accepted, M spawned

## Slices

### Phase Transitions
- **Slice Name**: Phase A -> Phase B
- **Slice Name**: Completed (date)

### Decisions & Direction Changes
- **Slice Name** — ADR-N: Title
- **Slice Name** — what changed (few words)

### New Slices
- **Slice Name** from Effort Name — scope (few words)

## Forge Infrastructure
- Brief bullets of meaningful changes only

## Dig Deeper

- [Description](path/to/file.md)
```

## Output Rules

- **Maximize scannability, minimize reading time.** Each
  item states *what happened* in the fewest words possible.
  No rationale, no justification, no "because" clauses.
- **Skip empty sections entirely** — no "None" placeholders
- **One line per item maximum** in the digest body
- **Bold item names** for scannability
- **No commit hashes or counts** — focus on meaning
- **Past tense** — report what happened, not what is
  happening
- **Use em dashes** (`—`) not hyphens for separators in
  item descriptions
- **Dig Deeper links** must be full paths or GitHub URLs
  that readers can navigate to — digests are often read
  outside Claude where relative paths don't resolve
- Digests are **ephemeral** — present directly, do not
  write to artifact files
- **Forge signature** — append the standard project SHA
  signature at the end of every digest using
  Skill: `forge-signature`
