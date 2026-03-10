---
name: evidence-based-analysis
description: >-
  This skill should be used when presenting
  "investigation findings", "design decisions",
  "code review feedback", or any analysis that requires
  structured evidence. Provides evidence tables,
  confidence levels (High/Med/Low), fact vs speculation
  separation, and source citation patterns.
---

# Evidence-Based Analysis

Structured patterns for gathering facts, analyzing evidence,
and presenting findings in investigation and design work.

## Core Principle

**Facts before opinions. Evidence before actions.**

Present what you observed, cite your sources, and distinguish
certainty from speculation. Let evidence drive conclusions, not
assumptions.

## When to Use This Pattern

**Always use for:**
- Investigation findings (issue triage, root cause analysis)
- Design decisions (architectural choices, trade-offs)
- Code review feedback (concrete issues with evidence)
- Research summaries (external patterns, best practices)

**Pattern applies when:**
- Presenting findings that will inform user decisions
- Making claims that need verification
- Documenting analysis for future reference

## Evidence Table Format

Use structured tables to present findings clearly:

```markdown
| Finding | Source | Confidence |
|---------|--------|------------|
| {what was found} | {file, commit, issue, doc} | High/Med/Low |
| {what was found} | {file, commit, issue, doc} | High/Med/Low |
```

**Finding:** Concise statement of what you discovered

**Source:** Where the evidence came from:
- Code: `file.py:line` or `file.py:line-range`
- Git: `commit abc123` or `PR #123`
- Docs: `path/to/doc.md:section`
- External: `{URL}` or `{paper/blog title}`

**Confidence:** High, Medium, or Low (see below)

## Confidence Levels

Not all findings are equally certain. Be explicit:

| Level | Criteria | When to Use |
|-------|----------|-------------|
| **High** | Direct evidence (code, logs, commits, tests) | You read it yourself |
| **Medium** | Inferred from patterns (similar cases) | Based on precedent |
| **Low** | Possible based on architecture (hypothetical) | Educated guess |

### Confidence Level Examples

**High confidence:**
- "The git log shows commit abc123 changed file.py on 2026-02-15"
- "Function foo() at bar.py:42 raises ValueError when x < 0"
- "Test suite has 15 passing tests for auth module"

**Medium confidence:**
- "Likely related to the recent auth refactor"
- "Similar pattern exists in module X, probably applies here"
- "Based on the error message, this appears to be a JWT issue"

**Low confidence:**
- "May affect mobile clients (not verified)"
- "Possibly related to caching behavior (hypothesis)"
- "Could be a race condition (needs investigation)"

## Fact vs. Speculation

Clearly distinguish what you observed from what you infer:

### Facts (Observed Directly)

Things you can point to with evidence:

```
✅ Good examples:
- "The git log shows commit abc123 on 2026-02-15"
- "File auth.py:148 catches all exceptions without re-raising"
- "The API returns HTTP 500 for invalid tokens"
```

**Characteristics:**
- Verifiable by reading code, logs, tests, or docs
- No interpretation needed
- Specific file:line or commit references

### Speculation (Inferred, Needs Verification)

Things you conclude based on evidence:

```
✅ Good examples (marked clearly):
- "Hypothesis: The refactor broke token validation"
- "Likely cause: The recent auth changes introduced this"
- "Assumption: Mobile clients use the same endpoint"
```

**Characteristics:**
- Requires interpretation
- Explicitly marked (Hypothesis, Likely, Assumption, Possibly)
- Should be verified before relying on it

```
❌ Bad examples (unmarked speculation):
- "This is probably broken"
- "The auth module doesn't work"
- "Users will be confused"
```

**Why bad?** Presents speculation as fact. Reader can't tell if
you verified this or are guessing.

## Structured Presentation Patterns

### Investigation Findings

For issue investigation or root cause analysis:

```markdown
## Summary

{2-3 sentence executive summary}

## Evidence

| Finding | Source | Confidence |
|---------|--------|------------|
| {finding 1} | {source} | High/Med/Low |
| {finding 2} | {source} | High/Med/Low |

## Analysis

{Reasoning from evidence to conclusions}

## Recommendations

1. {Highest priority action}
2. {Second priority action}
3. {Lower priority or optional action}
```

### Design Decisions

For architectural or technical choices:

```markdown
## Decision: {What are we deciding}

**Context:** {Why is this decision needed?}

**Options Considered:**

1. **{Option A}**
   - **Pros:** {Advantages}
   - **Cons:** {Disadvantages}
   - **Evidence:** {Prior art, constraints}

2. **{Option B}**
   - **Pros:** {Advantages}
   - **Cons:** {Disadvantages}
   - **Evidence:** {Prior art, constraints}

**Decision:** {What we chose and why}

**Consequences:** {Trade-offs we're accepting}

**Verification:** {How we'll know this was the right choice}
```

### Code Review Feedback

For providing review comments with evidence:

```markdown
## Code Review Findings

### Critical Issues (Must Fix)

**Item 1: {Title}**
- **File:** {file}:{line}
- **Issue:** {What's wrong}
- **Evidence:** {Why it's wrong — error condition, contract}
- **Fix:** {Recommended solution}

### Important Issues (Should Fix)

**Item 2: {Title}**
...

### Minor Issues (Nice to Have)

**Item 3: {Title}**
...
```

See Skill: `code-review-structure` for complete review patterns
and severity classification.

## Citing Sources

Always cite where information came from:

### Code Sources

```
# Pattern: file:line or file:line-range
src/auth/api.py:148
src/auth/api.py:142-156
```

### Git Sources

```
# Commit reference
Commit abc123d (2026-02-15): "refactor: Simplify auth handling"

# PR reference
PR #123: "Add token expiration handling"
```

### Documentation Sources

```
# Context files
.forge-context/context/product.md (Integration Points section)

# External docs
https://jwt.io/introduction (JWT structure and validation)
```

## Common Patterns and Anti-Patterns

### Good: Evidence-First Presentation

"The git log shows commit d4e5f6g on 2026-02-10 refactored
auth/api.py:148-150. The new exception handler catches
InvalidTokenError without re-raising, causing 500 instead of
401. High confidence — verified by reading commit diff and
current code."

### Good: Explicit Confidence Levels

| Finding | Source | Confidence |
|---------|--------|------------|
| Handler catches InvalidTokenError | auth/api.py:148 | High |
| Introduced in refactor | git show d4e5f6g | High |
| May affect mobile clients | Arch assumption | Low |

### Bad: Vague Claims Without Evidence

"The auth module is broken."

**Why bad?** No evidence, no specifics. What's broken? Where?
How do you know?

### Bad: Speculation Presented as Fact

"Users will be confused by this error message."

**Why bad?** You haven't asked users. Say: "Hypothesis: Users
may find this error message unclear (needs user testing)."

## Summary

| Aspect | Pattern | Purpose |
|--------|---------|---------|
| **Evidence table** | Finding → Source → Confidence | Structured fact presentation |
| **Confidence levels** | High/Med/Low | Clear uncertainty communication |
| **Fact vs. speculation** | Explicit markers | Prevent misleading claims |
| **Source citation** | file:line, commits, docs | Verifiable references |
| **Structured presentation** | Summary → Evidence → Analysis → Recommendations | Logical flow |

**Key principle:** Evidence drives conclusions. Cite sources,
distinguish facts from inferences, and provide confidence levels.
