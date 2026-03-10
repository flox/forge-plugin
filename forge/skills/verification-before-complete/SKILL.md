---
name: verification-before-complete
description: >-
  This skill should be used when completing tasks,
  "marking done", "claiming success", or before reporting
  any work as finished. Provides evidence-based completion
  discipline with test output, build logs, and manual
  testing patterns. Do not use for planning tests (see
  testing-strategy) or the TDD cycle (see tdd-discipline).
---

# Verification Before Complete

Evidence-based completion discipline adapted for Forge workflows.
Prevents false "done" claims by requiring concrete verification
before marking tasks complete or claiming success.

## Core Principle

**"Done" means "verified", not "attempted".**

Before claiming a task is complete, provide evidence that it
actually works. This prevents:
- False confidence (claimed done but actually broken)
- Wasted reviewer time (PR doesn't work as described)
- Deployment failures (untested code reaches production)

## The Verification Requirement

### What Counts as Verification?

**Acceptable evidence:**
- Test output showing tests pass
- Build logs showing successful compilation
- Screenshots or recordings of manual testing
- CLI output demonstrating feature works
- Integration test results

**Not acceptable:**
- "I think it works"
- "Should be fine"
- "Tests probably pass"
- "Looks good to me"

### When Verification is Required

| Scenario | Verification Type |
|----------|-------------------|
| **Code changes** | Run tests, show output |
| **Build changes** | Build succeeds, show logs |
| **Config changes** | Apply config, show result |
| **Documentation** | Render docs, check formatting |
| **Bug fixes** | Reproduce bug, show fix works |
| **Refactors** | Tests still pass (no behavior change) |

## Verification Workflow

### Step 1: Complete the Work

Implement the feature, fix the bug, or make the change.

### Step 2: Run Verification

**For Python projects:**
```bash
# Run tests
pytest path/to/test_file.py

# Expected output to capture:
# ====== X passed in Y.YYs ======
```

**For JavaScript/TypeScript projects:**
```bash
# Run tests
npm test

# Expected output to capture:
# Tests: N passed, N total
```

**For any project:**
```bash
# Check the project's CLAUDE.md for the test command
# Common patterns:
just test
just {project} test
npm test
pytest
```

### Step 3: Capture Evidence

**In commit messages:**
```
feat(manifest): Add version 2.0 validation

Implementation: Added validate_manifest function
Testing: pytest shows all tests pass

Test output:
  running 12 tests
  ...
  ====== 12 passed in 0.45s ======
```

**In PR descriptions:**
```
## Verification

### Unit Tests
$ pytest
====== 15 passed in 1.23s ======

### Manual Testing
Tested with:
- Valid input → Success
- Invalid input → Clean error message
- Missing field → Helpful error

All scenarios work as expected.
```

### Step 4: Mark Complete

Only after capturing verification evidence should you:
- Mark ticket/task as done
- Claim "implementation complete" in status updates
- Request code review (for PRs)

## Common Verification Patterns

### Pattern 1: Test-Driven Work

**When using TDD (see `tdd-discipline` skill):**

Already have verification evidence:
- RED: Test failed (proof it tests something)
- GREEN: Test passes (proof feature works)
- REFACTOR: Tests still pass (proof refactor didn't break)

Just include test output in commit/PR.

### Pattern 2: Integration Work

**When integrating multiple components:**

Verify each integration point:
1. Component A works (test directly)
2. Component B consumes A (test the interaction)
3. End-to-end flow (test full scenario)

### Pattern 3: Bug Fixes

**When fixing a bug:**

1. Reproduce the bug (capture error)
2. Apply fix
3. Verify bug no longer occurs (capture success)

**Example:**
```
## Bug Reproduction (BEFORE)
$ run-command
Error: KeyError: 'missing_field'

## After Fix
$ run-command
Success: processed 3 items
```

### Pattern 4: Refactoring

**When refactoring without behavior change:**

Run full test suite before and after:

```
## Refactor Verification
Before refactor: pytest → 45 passed
After refactor: pytest → 45 passed

No behavior change; tests confirm identical behavior.
```

## Verification Levels

### Level 1: Unit Tests (Minimum)

Every code change should have unit test coverage.

```
Verification: Unit tests pass
$ pytest tests/unit/test_module.py
====== 8 passed in 0.12s ======
```

### Level 2: Integration Tests (Recommended)

For changes affecting multiple components or contracts.

```
Verification: Integration tests pass
$ pytest tests/integration/
====== 12 passed in 3.45s ======
```

### Level 3: Manual Testing (Critical Features)

For user-facing features or critical paths.

```
Verification: Manual testing
Scenarios tested:
- Primary user flow → ✅ works
- Error path → ✅ handled gracefully
- Edge case → ✅ handled correctly
```

## Exceptions to Verification

### When Verification May Be Skipped

**Very rare cases where verification is impractical:**

1. **Typo fixes in documentation**
   - Visual inspection suffices
   - Example: "Fix typo in README: 'teh' → 'the'"

2. **Comment changes only**
   - Code comments (not doc comments)
   - Example: "Clarify comment in validation logic"

3. **Purely cosmetic changes**
   - Formatting if linter passes
   - Example: "Run formatter on codebase"

**Note:** If in doubt, verify. Skipping verification is the
exception, not the rule.

## Anti-Patterns to Avoid

### Claiming Success Without Evidence

```
❌ Bad:
"Implementation complete! Tests should pass."
(No evidence provided, reviewer has to test)

✅ Good:
"Implementation complete. Verification:
$ pytest
====== 15 passed in 0.45s ======
All tests pass as expected."
```

### Rationalization Without Testing

```
❌ Bad:
"Changed line 42 from X to Y. This should fix the bug
because [long explanation of why it should work]."
(No actual verification that it works)

✅ Good:
"Changed line 42 from X to Y.
Verification:
$ pytest tests/test_bug_scenario.py
====== 1 passed in 0.12s ======
Bug no longer reproduces."
```

### Partial Verification

```
❌ Bad:
"Ran one test manually, looks good."
(Only tested happy path, didn't run full suite)

✅ Good:
"Ran full test suite:
$ pytest
====== 45 passed in 2.1s ======
Also manually tested error paths:
- Invalid input → clean error message ✅
- Missing field → helpful error ✅"
```

## Integration with Forge Workflows

### For `implementation-worker` Agent

**Before marking task complete:**

1. Run appropriate tests (unit, integration, manual)
2. Capture test output
3. Include in commit message or PR description
4. Update ticket status with verification evidence
5. Only then mark task "Done"

**Example task update:**
```
Status: ✅ Complete

Verification:
- Unit tests: pytest → 12 passed
- Integration: Tested full flow → success
- Manual: Verified feature works end-to-end

Ready for review.
```

### For `code-reviewer` Agent

**When reviewing PRs:**

Check for verification evidence:
- [ ] PR description includes test output or verification steps
- [ ] Test output shows tests actually pass
- [ ] Manual testing described (if applicable)

**Red flags:**
- No verification evidence in PR
- Merge request with failing CI

**Request verification if missing:**
```
Requesting verification evidence:
- Please run tests and include output
- Manually test the primary flow and capture results
- Ensure CI passes before merging
```

## Documenting Verification

### In Commit Messages

```
feat(feature-name): Brief description

Implementation: {what was implemented}
Testing: {tests run}
Output: {relevant test output or success message}

Result: All tests pass, feature verified working.
```

### In PR Descriptions

```
## Verification

### Automated Tests
$ pytest
====== 15 passed in 0.45s ======

### Manual Testing
- Scenario 1: {description} → ✅ Success
- Scenario 2: {description} → ✅ Success
- Edge case: {description} → ✅ Handled

All verification passed. Ready for review.
```

## Summary

| Principle | Meaning |
|-----------|---------|
| **Done = Verified** | Don't claim complete without evidence |
| **Run tests, read output** | Actually check that tests pass |
| **Manual test critical paths** | Automated + human verification |
| **Capture evidence** | Include test output in commits/PRs |
| **No rationalization** | Evidence beats explanation |

**Key question before marking complete:**
> "If I showed this PR to a skeptical reviewer, could they
> see concrete evidence that it works?"

If the answer is no, you're not done yet.
