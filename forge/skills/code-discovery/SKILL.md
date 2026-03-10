---
name: code-discovery
description: >-
  This skill should be used when exploring code in a
  project for "investigation", "design research",
  "finding what changed", "git log analysis", or
  "finding precedent". Provides git log analysis, code
  reading strategies, and file:line reference patterns.
  Do not use for Forge planning file reading.
---

# Code Discovery

Deep codebase research patterns for investigation and design
workflows. Provides consistent approaches to exploring code,
understanding recent changes, and finding precedents.

## Core Principle

Understand the code before proposing changes. Evidence from
actual implementation beats assumptions from documentation.

## When to Use This Pattern

**Always use for:**
- Investigation work (finding what changed, what broke, when)
- Design work (understanding integration points, patterns)
- Research-driven analysis (precedents, similar features)

**Pattern applies when:**
- Feature touches existing code you haven't seen
- Need to understand recent changes (git log analysis)
- Looking for similar features to follow as precedent
- Need concrete file:line references for proposals

## Git Log Analysis

### Configurable Timeframes

Adapt git log timeframe based on investigation context:

```bash
# For suspected regressions: when did it break?
git log --oneline --since="{timeframe}" -- {path}

# Common timeframes:
# --since="2 weeks ago"  - Default for general investigation
# --since="1 week ago"   - Recent regression
# --since="1 month ago"  - Longer history for unclear issues
# --since="2026-01-15"   - Specific date from interview
```

**Determine timeframe from context:**
- **Confirmed regression**: User knows when it broke → use date
- **Suspected regression**: User reports "recently" → 1-2 weeks
- **Unclear**: No timeline info → 2-4 weeks for broader scan

### Finding Relevant Commits

**By file/directory path:**
```bash
# Changes to specific file
git log --oneline --since="{timeframe}" -- path/to/file.py

# Changes to directory
git log --oneline --since="{timeframe}" -- src/module/
```

**By commit message pattern:**
```bash
# Find commits mentioning a keyword
git log --oneline --since="{timeframe}" --grep="{keyword}"
```

**With file stats:**
```bash
# Show files changed per commit
git log --oneline --stat --since="{timeframe}"
```

### Reading Commit Details

```bash
# Full commit message and diff
git show {commit-sha}

# Just the commit message
git log -1 {commit-sha}

# Files changed in that commit
git show --name-only {commit-sha}
```

## Code Reading Strategies

### Use Context Files as Entry Points

Before reading code directly, consult `.forge-context/context/`
for structural information:

| Context File | Use For |
|--------------|---------|
| `product.md` | System overview and architecture |
| `components.md` | Component entry points |

**Why context files first?** They summarize the project
structure and point you to the right starting files.

### Tracing Implementations from Interfaces

When you need to understand how something works:

1. **Start with the interface** (API endpoint, CLI command,
   public function)
2. **Trace the call chain** (what calls what, data flow)
3. **Read critical paths** (happy path + main error path)
4. **Note assumptions** (what must be true for this to work)

**Example: Tracing a command**

```bash
# 1. Find command definition (entry point)
grep -r "command.*{name}" src/

# 2. Read the handler function
# (use file:line from grep result)

# 3. Trace calls made by handler
grep -r "{function_name}" src/

# 4. Read implementations of called functions
```

### Finding Similar Features for Precedent

When designing a new feature, find similar existing features:

**By functionality:**
```bash
# Find similar error handling
grep -r "raise.*Error" src/ | grep "{context}"

# Find similar API endpoints
grep -r "router.{method}" src/
```

**By file naming patterns:**
```bash
# Find related modules
find src/ -name "*{keyword}*"
```

**Review similar feature:**
- How did they structure it?
- What patterns did they use?
- What errors did they define?
- How did they test it?

**Document precedent:**
> "Similar pattern exists in {file}:{line}. Follows approach X
> for Y. Will use same pattern for consistency."

## Documentation Patterns

### File:Line References

Always include file:line references for concrete findings:

```
Good:
The authentication check happens in auth/api.py:148

Bad:
The authentication happens somewhere in the auth module
```

**Format:** `path/to/file.py:line` or `path/to/file.py:range`

**Why?** Enables readers to verify findings and provides
clickable links in many editors.

### Confidence Levels for Findings

Not all findings are equally certain. Indicate confidence:

| Level | Criteria | Example |
|-------|----------|---------|
| **High** | Direct evidence in code/logs | "File X:Y raises AuthError" |
| **Medium** | Inferred from patterns | "Likely related to change Z" |
| **Low** | Possible based on architecture | "May involve component W" |

**Usage:**
```
| Finding | Source | Confidence |
|---------|--------|------------|
| Auth check at api.py:148 | Direct code read | High |
| Related to recent token changes | Git log pattern | Medium |
| May affect mobile client | Architecture docs | Low |
```

### Assumptions vs. Facts

Clearly separate what you observed from what you infer:

**Facts** (observed directly):
- "The git log shows commit abc123 changed file.py"
- "Function foo() at bar.py:42 raises ValueError when x < 0"

**Assumptions** (inferred, needs verification):
- "This likely broke when the auth refactor landed"
- "The mobile client probably uses this endpoint"

**Mark assumptions explicitly:**
- "Assumption: ..." (needs verification)
- "Hypothesis: ..." (testable claim)
- "Likely: ..." (inferred from context)

## Integration with Other Skills

### With `evidence-based-analysis`

Code discovery feeds evidence-based analysis:
1. **Code discovery** finds the facts (commits, code, patterns)
2. **Evidence-based analysis** structures findings for
   presentation
3. Both emphasize evidence over speculation

### With `systematic-debugging`

For investigation work, code discovery supports debugging:
- **Phase 1 (Root Cause)**: Git log + code reading to find cause
- **Phase 2 (Pattern)**: Search for similar errors in codebase
- **Phase 3 (Hypothesis)**: Code understanding informs predictions
- **Phase 4 (Fix)**: Know what to change and why

## Common Patterns and Anti-Patterns

### Good: Progressive Exploration

1. Read context files first (project summary)
2. Use git log to narrow timeframe
3. Read specific files identified by log
4. Trace from entry points to implementations
5. Document findings with file:line references

### Good: Concrete References

"The error handling in auth/api.py:148-150 catches all
exceptions, masking the specific validation error from line 142."

### Bad: Vague Assumptions

"The auth module is probably broken somewhere."

### Bad: Skipping Context

Directly grepping the codebase without reading project context
files first. Wastes time exploring the wrong areas.

### Bad: Unbounded Exploration

Reading every file without a search strategy. Use git log and
context files to narrow scope.

## Summary

| Phase | Tool | Purpose |
|-------|------|---------|
| **Context** | `.forge-context/context/` | Start at right place |
| **Timeline** | Git log | Find what changed and when |
| **Deep dive** | Code reading | Trace implementations |
| **Precedent** | Search patterns | Find similar features |
| **Documentation** | file:line refs | Verifiable findings |

**Key principle:** Evidence-driven exploration. Read code, trace
history, document findings with references. Avoid speculation —
verify assumptions by reading the actual implementation.
