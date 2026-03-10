---
name: document-update-discipline
description: >-
  This skill should be used when "applying PR feedback",
  "processing discussion conclusions", "updating
  requirements from meeting notes", or any update that
  touches requirements.md, design.md, design-approach.md,
  or decisions.md. Ensures content lands at the correct
  abstraction level and in the correct document.
---

# Document Update Discipline

How to process incoming changes from any source and correctly
route content to the right document at the right abstraction
level.

## When to Load This Skill

**Always load when:**
- Applying PR discussion conclusions to slice documents
- Processing meeting notes or transcript summaries
- Applying interactive review feedback
- Reversing or updating decisions that affect multiple docs
- Any update that touches requirements.md OR design.md

**The discipline applies regardless of which document is
currently in scope.** If a design-only PR produces a change
that belongs in requirements, update requirements too.

## Core Principle

**Translate between abstraction levels. Never copy-paste.**

When a reviewer says something, their words contain both the
WHAT (requirement/outcome) and the HOW (design/mechanism).
Your job is to separate these and route each to the correct
document.

## The Four Documents

| Document | Contains | Abstraction Level |
|----------|----------|-------------------|
| requirements.md | What, why, outcomes | Behavioral |
| design-approach.md | Which direction, why | Strategic |
| design.md | How, where, mechanisms | Implementation |
| decisions.md | Why we chose, ADR format | Rationale |

### The Litmus Test

For each piece of content, ask: **"Do we have a choice?"**

- **No choice** (external constraint, user need, business
  rule) → requirement
- **Strategic direction** (which path, broad trade-offs)
  → design-approach
- **We chose this approach** (from alternatives) → design
- **We chose AND it's significant** → design + decision ADR

### Signal Words

Content likely belongs in **requirements** when it contains:
- User-facing outcomes ("users can...", "the system must...")
- Behavioral constraints ("only successful builds...")
- Success criteria ("validated by...", "supports...")

Content likely belongs in **design-approach** when it contains:
- Direction language ("we should go with...",
  "the approach is...")
- Trade-off comparisons ("option A vs option B")
- Strategic rationale ("because of ecosystem patterns...")

Content likely belongs in **design** when it contains:
- Component names and allocations
- Schema/API references ("in the database", "API returns")
- Implementation mechanisms
- Architecture decisions ("tagged union", "pagination")

## Processing Input Sources

### Source Type 1: Short PR Comments

Single-thread discussions with clear conclusions.

**Process:**
1. Read the conclusion
2. Classify: requirement, design, or decision
3. Apply to the correct document
4. If the PR only covers one document but the change belongs
   in another, update both

### Source Type 2: PR with Many Open Discussions

Multiple unresolved threads on the same PR.

**Process:**
1. **Scan all threads first** — read every unresolved thread
   before applying any changes
2. **Identify themes** — group related threads
3. **Identify final positions** — some threads may supersede
   others
4. **Synthesize per-theme conclusions** — one conclusion per
   theme, not per thread
5. **Classify each conclusion** — requirement vs design vs
   decision
6. **Apply in one pass** — update all affected documents
   together

**Why scan first:** Thread 3 may reverse Thread 1's conclusion.
Applying Thread 1 first and Thread 3 later wastes effort.

### Source Type 3: Meeting Transcript or Summary

Long-form input from a meeting or conversation.

**This is the highest-risk source for conflation.** Meeting
discussions are nonlinear — participants explore, backtrack,
and refine positions throughout.

**Process:**

#### Step 1: Full Scan (MANDATORY)

Read the entire transcript/summary before extracting anything.
During the scan, note:
- Points where participants agree on something
- Points where a position is later reversed
- Points that reach no conclusion
- Supporting context and rationale

#### Step 2: Extract Final Conclusions

For each topic, identify the **final position** — the last
agreed-upon state, not intermediate positions:

```
Topic: [topic]
Final conclusion: [what was ultimately decided]
Reversed from: [earlier position, if any]
Supporting context: [rationale, examples, constraints]
Classification: requirement | design | decision
Confidence: high | medium | low
```

**Mark "low confidence" when:**
- Only one participant stated the position
- The conclusion was implicit, not explicit
- The discussion moved on without clear agreement

#### Step 3: Group and Reconcile

- Group conclusions by theme
- Check for contradictions between conclusions
- If a conclusion contradicts an existing document position,
  flag it as a decision reversal and prepare an ADR

#### Step 4: Classify and Route

For each conclusion, determine target document(s):

| If the conclusion is about... | Target |
|-------------------------------|--------|
| What the system must achieve | requirements.md |
| How the system achieves it | design.md |
| A significant choice with alternatives | decisions.md + affected doc |
| Strategic direction change | design-approach.md |
| A constraint imposed externally | requirements.md |

#### Step 5: Translate and Apply

For each conclusion, write it in the target document's
language:

**Example — reviewer says:**
> "The API should store all paths without checking for
> conflicts. The client handles conflict detection during
> lock time."

**This contains both a requirement and a design decision:**

requirements.md gets the outcome:
> "Path conflicts are detected and reported to users"

design.md gets the mechanism:
> "The API stores all published paths without server-side
> conflict prevention. The client detects conflicts during
> lock time and warns."

decisions.md gets the ADR:
> "D6: No Server-Side Conflict Detection — stores data for
> any path regardless of conflicts. Conflict logic is
> client-side."

## Boundary Verification (Post-Update Check)

After applying any updates, verify the boundary was maintained.

### Requirements.md Check

Scan requirements.md for implementation-language patterns.
If found in success criteria or scope sections, rewrite:

**Flag these patterns:**
- Component names: "catalog server", "client", "server"
- Allocation: "client-side", "server-side"
- Schema specifics: "in the database", "API returns"
- Implementation: "flat paginated", "tree building"

**Rewrite pattern:**
```
Before: "Database stores URL decomposed into base URL, ref,
         and rev as distinct components"
After:  "Source URL components (base URL, ref, rev) tracked
         to support the latest algorithm (D2, D4)"
```

### Design.md Check

Scan design.md for bare behavioral statements that match
requirements.md verbatim. Design should reference requirements,
not restate them.

**Rewrite pattern:**
```
Before: "Only successfully built packages appear in the catalog"
After:  "The CLI enforces D1 by only calling the API after a
         successful build completes"
```

## Decision Reversals

When a conclusion reverses an existing decision:

1. **Update decisions.md first** — supersede old ADR or add new
2. **Update design-approach.md** — if the reversal changes
   strategic direction
3. **Update design.md** — change the mechanism
4. **Update requirements.md** — change only the outcome, using
   the new decision number as reference

**Never apply the reversal language verbatim to requirements**
— translate to outcome level.

## Guardrails

### Out-of-Scope Document Changes

When a conclusion targets a document outside the current PR's
scope, **ask the user before applying.**

**In-scope** = any document already changed by the PR.
**Out-of-scope** = any document NOT changed by the PR.

> "This discussion conclusion belongs in {target_doc},
> which is not part of this PR:
>
> **Conclusion:** {brief summary}
> **Classified as:** {requirement | design | decision}
>
> Options:
> 1. Apply now (update {target_doc} in this branch)
> 2. Capture as follow-up (note in PR comment, apply later)
> 3. Skip (leave for human review)"

### Ambiguous Classification

When content doesn't clearly classify as requirement or design:

> "This conclusion could be either a requirement or design
> detail:
>
> **Content:** {the conclusion}
>
> **As a requirement:** {how it would read in requirements.md}
> **As design:** {how it would read in design.md}
>
> Which classification is correct?"

**Default when the user is unavailable:** classify as design.
Design documents tolerate more specificity, while requirements
documents are harmed by implementation leakage.

## Quick Reference Card

When processing any update, ask these five questions:

1. **What is the final conclusion?** (scan first, don't apply
   intermediate positions)
2. **Is this an outcome or a mechanism?** (litmus test: do we
   have a choice?)
3. **Which document does it belong in?** (outcome → req,
   mechanism → design, significant choice → decisions)
4. **Did I translate the language?** (reviewer words →
   document abstraction level)
5. **Is the target document in scope?** (if not, confirm with
   user before applying)
