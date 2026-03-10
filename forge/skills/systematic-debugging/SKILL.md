---
name: systematic-debugging
description: >-
  This skill should be used when debugging failures,
  "test is failing", "error I can't explain", "something
  broke", or any situation requiring structured diagnosis.
  Provides a 4-phase root-cause approach. Do not use for
  planning tests or writing new code.
---

# Systematic Debugging

A structured 4-phase approach to debugging that prevents wild
goose chases and thrashing. Adapted from proven debugging
methodologies for Forge workflows.

## Why Systematic Debugging Matters

**Anti-pattern (debugging thrash):**
- See error
- Try random fix
- Different error appears
- Try another random fix
- Repeat for hours
- Eventually fix by accident

**Systematic approach:**
- Understand root cause before fixing
- Form hypothesis before acting
- Validate hypothesis with evidence
- Fix with confidence

## The Four Phases

### Phase 1: Root Cause Analysis

**Goal:** Understand WHY the error is happening, not just
WHAT the error is.

**Actions:**
1. Read the full error message (don't skim)
2. Identify the exact line/function where failure occurs
3. Trace backward from failure point to find originating cause
4. Ask: "What assumption is being violated?"

**For Python errors:**
- Check stack trace for first application code (not library)
- Look for AttributeError, KeyError, TypeError patterns
- Verify models match migration state

**For TypeScript/JavaScript errors:**
- Read the type error explanation carefully
- Check for null/undefined access patterns
- Look for type mismatches in function calls

**For build errors:**
- Read the first error, not just the last one
- Check for missing imports or dependencies
- Look for version conflicts

**Output:**
```
Root Cause: {Specific reason the error occurs}
Evidence: {Error message, stack trace, or log showing this}
```

### Phase 2: Pattern Recognition

**Goal:** Identify if this is a known pattern or new failure
mode.

**Actions:**
1. Search codebase for similar error patterns
2. Check if this error has appeared in git history (might
   have been fixed before)
3. Look for existing error handling in related code
4. Ask: "Have we seen this category of error before?"

**Common patterns:**
- Path confusion (relative vs absolute paths)
- Context not loaded (accessing data before it exists)
- State mismatch (expecting something that isn't there)
- Git state confusion (expecting branch exists, but doesn't)

**Output:**
```
Pattern: {Known pattern name or "New failure mode"}
Similar cases: {Related errors or fixes in codebase}
```

### Phase 3: Hypothesis Formation

**Goal:** Form testable hypothesis BEFORE making changes.

**Actions:**
1. Based on root cause and pattern, predict what change will
   fix it
2. Identify how to test the hypothesis
3. Consider alternative hypotheses
4. Choose most likely hypothesis first

**Good hypothesis characteristics:**
- Specific (not "something's wrong with X")
- Testable (can verify if correct)
- Explains all symptoms (not just one error)

**Example hypotheses:**
```
❌ Bad: "The file path is wrong"

✅ Good: "The cd command failed silently because directory
doesn't exist, so subsequent commands run in wrong location"
```

**Output:**
```
Hypothesis: {Specific prediction of what will fix it}
Test: {How to verify if hypothesis is correct}
Expected outcome: {What should happen if hypothesis is right}
```

### Phase 4: Fix with Validation

**Goal:** Apply fix and verify it solves the problem without
creating new issues.

**Actions:**
1. Make minimal change to test hypothesis
2. Run test or reproduce error scenario
3. Verify fix solves original problem
4. Check for side effects or new errors
5. If hypothesis wrong, return to Phase 3 with new information

**Validation methods:**
- **Unit tests:** Run specific test that failed
- **Integration tests:** Run full test suite for affected module
- **Manual verification:** Reproduce original error scenario
- **Regression check:** Ensure no new errors introduced

**Anti-patterns:**
- Changing multiple things at once (can't tell what fixed it)
- Not verifying the fix (claiming success without evidence)
- Fixing symptom instead of root cause (band-aid fix)

**Output:**
```
Fix applied: {What changed}
Validation: {Test/verification performed}
Result: {Pass/Fail with evidence}
Side effects: {Any new issues observed}
```

## Debugging Workflow Example

### Scenario: Agent fails to navigate to worktree

**Phase 1: Root Cause**
```
Error: bash: cd: _worktrees/my-feature: No such file or directory

Root Cause: Relative path check succeeded (from repo root),
but cd failed (running from inside worktree).

Evidence:
- test -d "_worktrees/my-feature" returned success
- cd _worktrees/my-feature failed
- pwd showed /home/user/project/_worktrees/other-feature

The agent is already INSIDE a different worktree, so relative
path doesn't exist from there.
```

**Phase 2: Pattern**
```
Pattern: Path confusion — relative vs absolute paths
Similar cases: Common issue when shell CWD isn't repo root
Related: Always use absolute paths for worktree navigation
```

**Phase 3: Hypothesis**
```
Hypothesis: Using absolute paths from git worktree list will
work from any location, unlike relative paths.

Test: Replace relative check with:
  path=$(git worktree list | grep "my-feature" | awk '{print $1}')
  cd "$path"

Expected outcome: cd succeeds regardless of current location
```

**Phase 4: Fix**
```
Fix applied: Updated to use absolute paths from git worktree list

Validation: Ran from three locations:
  - Repo root: ✅ navigated successfully
  - Different worktree: ✅ navigated successfully
  - Target worktree: ✅ detected "already there"

Result: PASS — all scenarios work
Side effects: None observed
```

## When to Use This Pattern

**Always use for:**
- Test failures (don't guess why test failed)
- Runtime errors (understand before fixing)
- Build failures (trace compilation errors)
- Integration issues (API/contract mismatches)

**Optional for:**
- Typos or obvious mistakes (fix directly)
- Linter warnings (follow linter suggestion)
- Documentation updates (no debugging needed)

## Integration with Forge Workflows

**During implementation (`implementation-worker` agent):**
- When tests fail, document debugging phases in commit
  message or PR
- Don't claim "fixed" without validation phase evidence
- Reference which phase revealed the solution

**During code review (`code-reviewer` agent):**
- Check if PRs include validation evidence for fixes
- Verify root cause is addressed, not just symptoms

**In retrospectives:**
- Track patterns that appear repeatedly
- Update context/guidelines when new patterns emerge
- Improve error messages based on root cause insights

## Exceptions and Pragmatic Use

**When to skip systematic debugging:**
- Error message is self-explanatory ("file not found")
- Fix is one-line trivial change
- Debugging would take longer than trying obvious fix

**When to use lightweight version:**
- For simple errors: Root Cause + Fix (skip Pattern and
  Hypothesis)
- For known patterns: Pattern + Fix (leverage knowledge)

**Full 4-phase process recommended for:**
- Mysterious errors without obvious cause
- Errors that reappear after attempted fixes
- System integration failures (multi-component)

## Documenting Debugging Sessions

When debugging reveals important insights, document them:

**In commit messages:**
```
fix(agent): Prevent worktree navigation failures

Root cause: Agents used relative paths which only work from
repo root.
Pattern: Path confusion (relative vs absolute).
Fix: Use absolute paths from git worktree list.
Validated: Tested from repo root, other worktree, and target.
```

**In PR descriptions:**
```
## Debugging Summary
Root cause: {brief}
Fix: {what changed}
Validation: {tests run, output observed}
```

## Summary

| Phase | Question | Output |
|-------|----------|--------|
| 1. Root Cause | WHY is this failing? | Specific reason + evidence |
| 2. Pattern | Have we seen this before? | Pattern name or "new mode" |
| 3. Hypothesis | What change will fix it? | Testable prediction |
| 4. Fix | Does the fix work? | Validation evidence |

**Key principle:** Understand before acting.
Evidence before claiming success.
