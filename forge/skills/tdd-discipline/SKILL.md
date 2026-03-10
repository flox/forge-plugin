---
name: tdd-discipline
description: >-
  This skill should be used when performing test-driven
  development, "write a failing test first", "RED-GREEN-
  REFACTOR", or implementing new functionality with tests.
  Covers the full TDD cycle with pragmatic exceptions for
  generated code and configuration files. Do not use for
  planning testing strategy (see testing-strategy).
---

# TDD Discipline

Test-Driven Development discipline adapted for Forge workflows.
Follows the RED-GREEN-REFACTOR cycle where appropriate, with
pragmatic exceptions for generated code and configuration files.

## The RED-GREEN-REFACTOR Cycle

### 1. RED: Write a Failing Test

**Before writing implementation code, write a test that fails.**

**Why:**
- Proves the test actually tests something
- Prevents false positives ("test passes but feature doesn't work")
- Clarifies what "done" means before starting

**Actions:**
1. Write test for desired behavior
2. Run test — it should FAIL
3. Read failure message — confirm it fails for the right reason
4. If test passes unexpectedly, investigate why

**Example (Python):**
```python
def test_validate_manifest_version():
    manifest = Manifest(version="2.0")
    assert validate_manifest(manifest) is True
    # Run: pytest
    # Expected: FAIL - validate_manifest doesn't exist yet
```

### 2. GREEN: Make the Test Pass

**Write minimal code to make the test pass.**

**Why:**
- Focuses on solving the specific problem
- Avoids over-engineering
- Creates fast feedback loop

**Actions:**
1. Write simplest implementation that passes test
2. Run test — it should PASS
3. Read output — confirm test passes for right reason
4. Don't add extra features yet (that's refactor phase)

**Example (Python):**
```python
def validate_manifest(manifest):
    if manifest.version == "2.0":
        return True
    raise ValueError("Invalid version")
# Run: pytest
# Expected: PASS
```

### 3. REFACTOR: Improve Code Quality

**Clean up code while keeping tests passing.**

**Why:**
- Prevents technical debt accumulation
- Improves readability and maintainability
- Tests provide safety net for refactoring

**Actions:**
1. Look for duplication, unclear names, or poor structure
2. Refactor code
3. Run tests — they should still PASS
4. If tests fail after refactor, you broke something (fix it)

**Example (Python):**
```python
SUPPORTED_VERSION = "2.0"

def validate_manifest(manifest):
    if manifest.version != SUPPORTED_VERSION:
        raise ValueError(
            f"Unsupported version: {manifest.version}"
        )
    return True
# Run: pytest
# Expected: PASS (same behavior, clearer code)
```

## When to Use TDD

### Strong TDD Candidates

**Use full RED-GREEN-REFACTOR for:**

- Business logic (validation, transformation, calculation)
- Error handling (parsing errors, argument validation)
- Data transformations (converting between types)
- API handlers (request handling, response formatting)
- Service integrations (external calls, auth logic)

**Examples:**
- "Add validation for manifest version field"
  → Write failing test → Implement validator → Refactor
- "Parse package metadata"
  → Write failing test with sample data → Implement → Refactor

### TDD Optional (Consider Case-by-Case)

**TDD can help but isn't mandatory:**

- Integration tests (may be easier to write after
  implementation exists)
- UI components (visual verification often needed alongside)

### TDD Exceptions (Pragmatic Skips)

**Do NOT use TDD for:**

1. **Generated code**
   Code generators are tested separately. Testing generated
   output is redundant. Approach: test the generator, not its
   output.

2. **Configuration files**
   JSON, YAML, TOML configs. Approach: validate with schema
   or linter.

3. **Documentation**
   Markdown files. Approach: review for accuracy.

4. **Simple refactors**
   Renaming variables, moving functions. Existing tests
   provide coverage. Approach: run existing test suite.

## TDD in Forge Workflows

### For `implementation-worker` Agent

**When implementing a ticket:**

1. **Check if TDD applies** — review exceptions list above
2. **If TDD applies:**
   - Write test first (RED phase)
   - Note in commit/PR: "Wrote failing test first"
   - Implement feature (GREEN phase)
   - Refactor if needed (REFACTOR phase)
3. **If TDD exception:**
   - Implement feature
   - Write tests after (or skip if not applicable)
   - Note exception reason in commit

**Example commit message:**
```
feat(manifest): Add version validation

TDD approach:
- RED: Wrote test expecting version 2.0 validation
- GREEN: Implemented validate_manifest function
- REFACTOR: Extracted SUPPORTED_VERSION constant

Tests: pytest passes
```

### For `code-reviewer` Agent

**When reviewing PRs:**

Check for TDD evidence:
- Did PR include tests?
- For logic changes, were tests written first? (Check commit
  history)
- If no tests, is it a valid exception?

**Red flags:**
- Complex logic change with no tests
- Tests that always pass without testing behavior

**Acceptable:**
- "Generated code — generator is tested separately"
- "Simple refactor — existing tests provide coverage"

## Documenting TDD Approach

### In Commit Messages

```
feat(feature-name): Brief description

TDD: RED-GREEN-REFACTOR followed
- Test: {what test was written}
- Implementation: {what was implemented}
- Validation: {test output showing pass}
```

OR for exceptions:

```
feat(feature-name): Brief description

TDD exception: {reason}
- Generated code: Tested generator separately
```

### In PR Descriptions

```
## Testing Approach

- [x] TDD: Wrote failing tests first
- [x] Tests pass: output shows all pass
- [x] Refactored: Improved clarity while maintaining coverage

OR

- [ ] TDD: N/A (generated code)
- [x] Validated: Generator output matches expected schema
```

## Anti-Patterns to Avoid

### Testing After Claiming Done

```
❌ Bad:
1. Write implementation
2. Manually test once
3. Open PR as "done"
4. Reviewer asks: "Where are the tests?"
5. Scramble to add tests

✅ Good:
1. Write failing test
2. Implement until test passes
3. Open PR with tests included
```

### False Positive Tests

```
❌ Bad:
def test_feature():
    # Feature not implemented yet
    assert True  # Always passes, tests nothing

✅ Good:
def test_feature():
    result = my_function()
    assert result == expected_value
    # Run first — should FAIL (function doesn't exist)
```

## Pragmatic TDD: Balance Discipline with Delivery

**TDD is a discipline, not a religion.**

**Use TDD when it helps:**
- Complex logic that needs confidence
- Public APIs that need clear contracts
- Bug fixes (write failing test that reproduces bug first)

**Skip or adapt TDD when it doesn't:**
- Generated code (test generator instead)
- Simple changes (existing tests suffice)
- Exploratory prototyping (write tests once direction is clear)

**The key principle:**
> "If you haven't watched the test fail, you don't know if it
> works."

When you skip the RED phase, at least manually verify the
feature works and note that in your PR. Don't claim "done"
without evidence.

## Summary

| Phase | Action | Evidence |
|-------|--------|----------|
| RED | Write failing test | Test output shows failure |
| GREEN | Implement feature | Test output shows pass |
| REFACTOR | Clean up code | Tests still pass |

**Exceptions:** Generated code, configs, docs, simple refactors

**Key principle:** Watch the test fail before claiming it works.
