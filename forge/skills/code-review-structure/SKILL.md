---
name: code-review-structure
description: >-
  This skill should be used when performing a "code
  review", "PR review", "review pull request", or
  evaluating implementation quality. Provides a two-stage
  process: Stage 1 checks spec compliance (does it do
  what was designed?), Stage 2 checks quality (is the
  code good?). Includes C/I/M severity classification.
  Do not use for design reviews or requirements reviews.
---

# Code Review Structure

A two-stage code review process that prevents wasted effort and
improves review quality. Stage 1 validates spec compliance
before Stage 2 examines code quality.

## Why Two Stages?

**Problem with unstructured review:**
- Reviewer spends time on code quality
- Later discovers PR doesn't match requirements
- All quality feedback is wasted (needs redesign)

**Two-stage solution:**
1. **Spec compliance first** — Does this implement what was
   designed?
2. **Quality second** — Is the implementation good?

If Stage 1 fails, stop and address spec issues before quality
review.

## Stage 1: Spec Compliance

**Goal:** Verify PR matches requirements and design.

### Compliance Checklist

**Requirements Alignment:**
- [ ] PR addresses requirements from requirements.md
- [ ] Success criteria from requirements.md are met
- [ ] Scope matches (no out-of-scope additions)
- [ ] Edge cases from requirements are handled

**Design Alignment:**
- [ ] Implements design from design.md
- [ ] Architecture decisions followed (ADRs respected)
- [ ] API contracts match design
- [ ] Integration points match design

**Test Coverage Alignment:**
- [ ] Tests match testing strategy from design.md
- [ ] Unit tests for business logic
- [ ] Integration tests for component interactions

**Deliverable Completeness:**
- [ ] All tasks from ticket are complete
- [ ] No "TODO" or "FIXME" for in-scope work
- [ ] Documentation updated (if applicable)

### Spec Compliance Review Output

**If compliant:**
```
## Stage 1: Spec Compliance ✅

- Requirements: Aligned with specified criteria
- Design: Follows architecture from design.md
- Testing: All test types from strategy present
- Completeness: All ticket tasks addressed

Proceeding to Stage 2 (Quality Review).
```

**If non-compliant:**
```
## Stage 1: Spec Compliance ❌

Non-compliance issues (must fix before quality review):

1. Missing functionality: Requirement calls for version
   validation, but code only checks format, not values
2. Design mismatch: Design specified using existing Error
   type, but PR creates new error types
3. Test gap: Design called for integration tests, but
   only unit tests present

Action required: Address spec issues before re-requesting
review. Quality review will begin once spec compliance is
achieved.
```

**Key principle:** Don't proceed to Stage 2 if Stage 1 fails.
Spec compliance issues are blocking.

## Stage 2: Code Quality

**Goal:** Verify implementation is maintainable, secure, and
follows best practices.

Only start Stage 2 after Stage 1 passes.

### Quality Review Areas

**Code Structure:**
- Function/module organization
- Naming clarity
- Code duplication
- Complexity (cyclomatic complexity, nesting depth)

**Error Handling:**
- Errors are informative
- Error paths are tested
- No silent failures

**Security:**
- Input validation
- SQL injection prevention
- Authentication/authorization checks
- Secrets not hardcoded

**Performance:**
- No obvious inefficiencies (N+1 queries, redundant loops)
- Large data handling appropriate
- Resource cleanup (file handles, connections)

**Maintainability:**
- Comments where logic isn't self-evident
- Consistent style with codebase
- No commented-out code
- Dependencies justified

### Severity Classification

Assign severity to each quality issue for clear prioritization.

#### Critical (C) — Must Fix Before Merge

**Criteria:** Security vulnerability, data loss risk, or
production-breaking bug.

**Examples:**
- SQL injection vulnerability
- Hardcoded secrets
- Race condition in critical path
- Unhandled error that crashes service

**Action:** Block merge until fixed.

#### Important (I) — Should Fix, May Block Merge

**Criteria:** Significant maintainability issue, performance
problem, or deviation from established patterns.

**Examples:**
- Poor error messages (confuses users/developers)
- Missing tests for error paths
- Inefficient algorithm (N^2 when N is expected large)
- Ignoring established patterns

**Action:** Fix before merge, or create follow-up ticket if
truly can't fix now (rare).

#### Minor (M) — Nice to Have, Non-Blocking

**Criteria:** Cosmetic issue, stylistic preference, or
micro-optimization.

**Examples:**
- Variable naming could be slightly clearer
- Comment could be more detailed
- Function could be split (but isn't complex)
- Small code duplication (2-3 lines)

**Action:** Optional fix. Can address or defer. Doesn't block
merge.

### Quality Review Output

```
## Stage 2: Code Quality

### Critical Issues (Must Fix) - 0
None found.

### Important Issues (Should Fix) - 2

**I1: Missing error handling for API timeout**
Location: src/api/client.py:45
Severity: Important
Issue: HTTP client doesn't handle timeout, will hang
Recommendation: Add timeout, return clear error

**I2: Query in loop (N+1 problem)**
Location: src/handlers/list.py:78
Severity: Important
Issue: Fetches record for each item in loop
Recommendation: Fetch all records in single query

### Minor Issues (Nice to Have) - 1

**M1: Variable naming**
Location: src/utils/parse.py:12
Severity: Minor
Issue: Variable `x` could be named `manifest_version`
Recommendation: Rename for clarity (optional)

---

Overall: 2 Important issues block merge. Please address
before approval.
```

## Review Workflow

### Step 1: Read Context

**Before reviewing code:**
1. Read `requirements.md` (what we're building)
2. Read `design.md` (how we're building it)
3. Read ticket description (specific task)
4. Understand acceptance criteria

### Step 2: Stage 1 Review (Spec Compliance)

**Review order:**
1. Check requirements coverage
2. Check design adherence
3. Check test strategy compliance
4. Check deliverable completeness

**Decision point:**
- Compliant → Proceed to Stage 2
- Non-compliant → Stop, request spec fixes, do NOT review
  quality

### Step 3: Stage 2 Review (Quality)

**Only if Stage 1 passed.**

**Review order:**
1. Security (Critical issues)
2. Correctness (Critical/Important)
3. Error handling (Important)
4. Performance (Important)
5. Maintainability (Important/Minor)
6. Style (Minor)

### Step 4: Provide Feedback

**Use structured format:**

```
## Code Review: {PR Title}

### Stage 1: Spec Compliance
[✅ Pass / ❌ Fail]
{Details}

### Stage 2: Code Quality
[Only if Stage 1 passed]

Critical: {count}
Important: {count}
Minor: {count}

{Detailed issues with severity labels}

---

Decision: [Approve / Request Changes]
Reason: {Why}
```

## Anti-Patterns to Avoid

### Quality Review Before Spec Check

```
❌ Bad:
Review focuses on code style, variable names, function
structure. Near end: "Wait, this doesn't implement the
key requirement at all!" All prior feedback is wasted.

✅ Good:
First check: Does this match requirements and design?
If no: Stop, request spec fixes.
If yes: Then review code quality.
```

### Severity Confusion

```
❌ Bad:
"Minor issue: SQL injection vulnerability"

✅ Good:
"CRITICAL: SQL injection vulnerability in user input
handling" (correct severity, blocks merge)
```

## Integration with Forge Workflows

### For `code-reviewer` Agent

**When reviewing a PR:**

1. **Load context** — Read requirements.md, design.md, ticket
2. **Stage 1 check** — Requirements, design, tests, completeness
3. **If Stage 1 fails** — Document non-compliance, request
   fixes, do NOT proceed to Stage 2
4. **If Stage 1 passes** — Proceed to Stage 2 quality review,
   classify by severity (C/I/M), provide structured feedback

### For PR Authors (Developers)

**Before requesting review:**

**Self-review Stage 1:**
- [ ] I've addressed all requirements from requirements.md
- [ ] My implementation follows design from design.md
- [ ] Tests match testing strategy
- [ ] All ticket tasks complete

**Self-review Stage 2:**
- [ ] No security vulnerabilities
- [ ] Error handling is robust
- [ ] Code is readable and maintainable
- [ ] Performance is acceptable

## Summary

| Stage | Focus | Blocking? | Output |
|-------|-------|-----------|--------|
| **Stage 1** | Spec compliance | Yes | ✅ Pass / ❌ Fail |
| **Stage 2** | Code quality | Severity-dependent | C/I/M issues |

**Key principles:**
1. Spec compliance before quality
2. Classify severity (Critical/Important/Minor)
3. Block merge on Critical issues
4. Provide structured feedback
